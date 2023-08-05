import datetime
import shutil
import sys
import time
import os
from typing import List, Tuple, Dict
from types import FunctionType
from fast_diff_py.utils import *
import multiprocessing as mp
import multiprocessing.connection as con
import threading as th
from fast_diff_py.datatransfer import *
from concurrent.futures import ProcessPoolExecutor
from fast_diff_py.sql_database import SQLiteDatabase
from fast_diff_py.config import FastDiffPyConfig
from fast_diff_py.fast_diff_base import FastDiffPyBase
from fast_diff_py.child_processes import parallel_resize, parallel_compare, find_best_image
from fast_diff_py.child_processes import first_loop_dequeue_worker, first_loop_enqueue_worker
from fast_diff_py.child_processes import second_loop_dequeue_worker, second_loop_enqueue_worker
from fast_diff_py.mariadb_database import MariaDBDatabase
import logging
import signal


"""
Fast implementation of the DifPy Library.
Features:
- Use GPU to accelerate the comparison
- Use Parallelization on multicore CPUs
- Use of aspect ration to ignore images with non-matching aspect ratio
- Use hash based deduplication to find duplicates with color grading
"""

# from contextlib import redirect_stdout
#
# with open('out.txt', 'w') as f:
#     with redirect_stdout(f):
#         print('data')



# TODO single processing handler
# TODO Implement process stop recovery.
# TODO plot table is redundant. Use key from diff table and if create plot insert an empty row in the diff table.
# TODO bulk processing first loop.
# ----------------------------------------------------------------------------------------------------------------------
# FEATURES
# ----------------------------------------------------------------------------------------------------------------------
# TODO Range in which the aspects must lay for matching_aspect to trigger
# TODO Harakiri method. More reckless method.
# TODO keyboard shortcuts pyinput
# TODO different shift amounts for different colors.
# TODO Arbitrary hash matching function
# TODO Extract hashing_data
# TODO Smart child processes that fetch their info from the db and that have a queue for the next key that needs ot be
#  processed. => Wont allow for smart algo for increment => for very large datasets. (Maybe with check?)



class FastDifPy(FastDiffPyBase):
    # relative to child processes
    first_loop_in: mp.Queue = None  # the tasks sent to the child processes
    first_loop_out: mp.Queue = None  # the results coming from the child processes

    second_loop_in: Union[List[mp.Queue], mp.Queue] = None
    second_loop_out: mp.Queue = None

    # multiprocessing handles
    cpu_handles = None
    gpu_handles = None

    # logger / CLI Output
    logger: logging.Logger = None
    file_handler: logging.FileHandler = None
    stream_handler: logging.StreamHandler = None
    debug_logger: logging.FileHandler = None

    loop_run: bool = False
    en_com_1: Union[None, con.Connection] = None
    de_com_1: Union[None, con.Connection] = None

    def __init__(self, directory_a: str, directory_b: str = None, default_db: bool = True, **kwargs):
        """
        Provide the directories to be searched. If a different implementation of the database is used,
        set the test_db to false.

        :param directory_a: first directory to search for differentiation.
        :param directory_b: second directory to compare against. Otherwise, comparison will be done against directory
        :param default_db: create a sqlite database in the a_directory.
        itself.

        kwarg:
        ------
        - debug: bool - Enable Debug File in the logs.
        - config_path: str - Path to the config that stores the progress of the program (for progress recovery on stop)
        - config_purge: str - Ignore preexisting config and overwrite it.
        - config: FastDiffPyConfig - Pass a preexisting config. (process recovery)
                                      Ignores config_path, config_purge kwarg!!!
        """
        super().__init__()

        if "config" in kwargs.keys():
            if type(kwargs.get("config")) is not FastDiffPyConfig:
                raise ValueError(f"Unsupported type for config: {kwargs.get('config').__name__}, "
                                 f"only FastDiffPyConfig allowed")
            self.config = kwargs.get("config")

            if self.config.database["type"] == "sqlite":
                self.db = SQLiteDatabase(path=self.config.database["path"])
            elif self.config.database["type"] == "mariadb":
                self.db = MariaDBDatabase(
                    user=self.config.database["user"],
                    password=self.config.database["password"],
                    host=self.config.database["host"],
                    port=self.config.database["port"],
                    database=self.config.database["database"],
                    table_suffix=self.config.database["table_suffix"]
                )

            return

        if not self.verify_config():
            # Only set the directory_a and directory_b when the config is not set.
            if not os.path.isdir(directory_a):
                raise NotADirectoryError(f"{directory_a} is not a directory")

            if directory_b is not None and not os.path.isdir(directory_b):
                raise NotADirectoryError(f"{directory_b} is not a directory")

            directory_a = os.path.abspath(directory_a)
            directory_b = os.path.abspath(directory_b) if directory_b is not None else None

            # make sure the paths aren't sub-dirs of each other.
            if directory_b is not None:
                temp_a = directory_a + os.sep
                temp_b = directory_b + os.sep
                if temp_a.startswith(temp_b):
                    raise ValueError(f"{directory_a} is a subdirectory of {directory_b}")
                elif temp_b.startswith(temp_a):
                    raise ValueError(f"{directory_b} is a subdirectory of {directory_a}")

            self.config.p_root_dir_b = directory_b
            self.config.p_root_dir_a = directory_a

            # Creating default database if desired.
            if default_db:
                self.db = SQLiteDatabase(path=os.path.join(self.config.p_root_dir_a, "diff.db"))

            self.config.ignore_paths = []
            self.config.ignore_names = []


        debug = False
        if "debug" in kwargs.keys():
            debug = kwargs.get("debug")

        self.prepare_logging(debug=debug)

        # Setting the first stuff in the config
        self.config.state = "init"
        self.config.write_to_file()

    def interrupt_handler(self):
        """
        Adds handlers for sigint and sigterm
        :return:
        """
        signal.signal(signal.SIGINT, self.sig_int)
        signal.signal(signal.SIGTERM, self.sig_int)

    def sig_int(self):
        """
        Handler to trigger the stopping of the loop functions.
        :return:
        """
        self.loop_run = False

        if self.en_com_1 is not None:
            self.en_com_1.send(Messages.Stop)

        if self.de_com_1 is not None:
            self.de_com_1.send(Messages.Stop)

        self.logger.info("Stop signal received, shutting down...")

    def verify_config(self, full_depth: bool = False):
        """
        Load the config and verify that the folders match and the content if the directories too.

        :param full_depth: Check that every file in the database exists.

        :return: returns False if no Config is found. otherwise returns true.
        """
        # Empty dict, we have nothing.
        if not os.path.exists(self.config.cfg_path):
            return False

        if full_depth:
            self.verify_dir_content()
        return True

    def verify_dir_content(self):
        """
        Function should go through dir table and make sure every file exists. If a file doesn't exist, raises ValueError.
        :return:
        """
        pass

    def index_the_dirs(self):
        """
        List all the files in directory_a and possibly directory_b and store the paths and filenames in the temporary
        database.

        :return:
        """
        self.__recursive_index(True)
        if self.config.has_dir_b:
            self.__recursive_index(False)

        self.config.state = "indexed_dirs"

        # get the number of images and create short circuit.
        im_num = self.db.get_dir_count()
        a_num = self.db.get_dir_count(dir_a=True)
        self.config.enough_images_to_compare = im_num > 1 and a_num >= 1
        self.config.write_to_file()

    def __recursive_index(self, dir_a: bool = True, path: str = None, ignore_thumbnail: bool = True):
        """
        Recursively index the directories. This function is called by the index_the_dirs function.

        :param ignore_thumbnail: If any directory at any level, starting with .temp_thumb should be ignored.
        :param dir_a: True -> Index dir A. False -> Index dir B
        :param path: The path to the current directory. This is used for recursion.
        :return:
        """

        # load the path to index from
        if path is None:
            if dir_a:
                path = self.config.p_root_dir_a
            else:
                path = self.config.p_root_dir_b

        for file_name in os.listdir(path):
            full_path = os.path.join(path, file_name)

            # ignore a path if given
            if full_path in self.config.ignore_paths:
                continue

            # ignoring based only on name
            if file_name in self.config.ignore_names:
                continue

            # Thumbnail directory is called .temp_thumbnails
            if file_name.startswith(".temp_thumb") and ignore_thumbnail:
                continue

            # for directories, continue the recursion
            if os.path.isdir(full_path):
                self.__recursive_index(dir_a, full_path)

            if os.path.isfile(full_path):
                # check if the file is supported, then add it to the database
                if os.path.splitext(full_path)[1].lower() in self.config.supported_file_types:
                    self.db.add_file(full_path, file_name, dir_a)

    def estimate_disk_usage(self, print_results: bool = True) -> Tuple[int, int]:
        """
        Estimate the diskusage of the thumbnail directory given the compressed image size.

        :param print_results: print the results to console
        :return: byte_count_a, byte_count_b
        """
        dir_a_count = self.db.get_dir_count(True)
        dir_b_count = self.db.get_dir_count(False)

        if dir_b_count == 0:
            comps = dir_a_count * (dir_a_count-1) / 2
        else:
            comps = dir_a_count * dir_b_count

        byte_count_a = dir_a_count * self.config.thumbnail_size_x * self.config.thumbnail_size_y * 3
        byte_count_b = dir_b_count * self.config.thumbnail_size_x * self.config.thumbnail_size_y * 3

        dir_b = self.config.p_root_dir_b if self.config.has_dir_b else ""

        target = max(len(self.config.p_root_dir_a), len(dir_b), len('the two dirs '))

        if print_results:
            print(
                f"Estimated disk usage by {fill(self.config.p_root_dir_a, target)}: " + h(byte_count_a, "B") +
                " bytes")
            if self.config.has_dir_b:
                print(
                    f"Estimated disk usage by {fill(self.config.p_root_dir_b, target)}: " + h(byte_count_b, "B") +
                    " bytes")
                print(f"Estimated disk usage by {fill('the two dirs ', target)}: " +
                      h(byte_count_b + byte_count_a, "B") + "bytes")

            print(f"Number of Images in Database {dir_a_count + dir_b_count}, Comparisons: {comps}")

        return byte_count_a, byte_count_b

    def clean_up(self, thumbs: bool = True, db: bool = True, config: bool = True):
        """
        Remove thumbnails and db.

        :param thumbs: Delete Thumbnail directories
        :param db: Delete Database
        :param config: Delete the Config file.
        :return:
        """
        if thumbs:
            self.logger.info("Deleting Thumbnails")
            try:
                shutil.rmtree(self.config.thumb_dir_a)
                self.logger.info(f"Deleted {self.config.thumb_dir_a}")
            except FileNotFoundError:
                pass
            if self.config.has_dir_b:
                try:
                    shutil.rmtree(self.config.thumb_dir_b)
                    self.logger.info(f"Deleted {self.config.thumb_dir_b}")
                except FileNotFoundError:
                    pass

        if db:
            self.db.free()
            self.db.disconnect()
            self.db.free()
            self.db = None
            self.logger.info("Deleted temporary database")

        if config:
            cfg_path = self.config.cfg_path
            self.config = None

            if os.path.exists(cfg_path):
                os.remove(cfg_path)
                self.logger.info("Deleted Config")

    # ==================================================================================================================
    # COMMON LOOP FUNCTIONS
    # ==================================================================================================================

    def check_create_thumbnail_dir(self):
        """
        Create the thumbnail directories if they don't exist already.

        :return:
        """
        if not os.path.exists(self.config.thumb_dir_a):
            os.makedirs(self.config.thumb_dir_a)

        if self.config.has_dir_b and not os.path.exists(self.config.thumb_dir_b):
            os.makedirs(self.config.thumb_dir_b)

    def send_termination_signal(self, first_loop: bool = False):
        """
        Sends None in the queues to the child processes, which is the termination signal for them.

        :param first_loop: if the termination signal needs to be sent to the children of the first or the second loop
        :return:
        """
        if first_loop:
            for i in range((len(self.cpu_handles) + len(self.gpu_handles))):
                self.first_loop_in.put(None)
            return

        if self.config.less_optimized:
            for i in range((len(self.cpu_handles) + len(self.gpu_handles))):
                self.second_loop_in.put(None)
            return

        [q.put(None) for q in self.second_loop_in]

    def join_all_children(self):
        """
        Check the results of all spawned processes and verify they produced a True as a result ergo, they computed
        successfully.

        :return:
        """
        cpu_proc = len(self.cpu_handles)

        # all processes should be done now, iterating through and killing them if they're still alive.
        for i in range(len(self.cpu_handles)):
            p = self.cpu_handles[i]
            try:
                self.logger.info(f"Trying to join process {i} Process Alive State is {p.is_alive()}")
                p.join(1)
                if p.is_alive():
                    self.logger.info(f"Process {i} timed out. Alive state: {p.is_alive()}; killing it.")
                    p.kill()
            except TimeoutError:
                self.logger.warning(f"Process {i} timed out. Alive state: {p.is_alive()}; killing it.")
                p.kill()

        for i in range(len(self.gpu_handles)):
            p = self.gpu_handles[i]
            try:
                self.logger.info(f"Trying to join process {i + cpu_proc} Process State is {p.is_alive()}")
                p.join(1)
                if p.is_alive():
                    self.logger.info(f"Process {i} timed out. Alive state: {p.is_alive()}; killing it.")
                    p.kill()
            except TimeoutError:
                self.logger.warning(f"Process {i + cpu_proc} timed out. Alive state: {p.is_alive()}; killing it.")
                p.kill()

    # ------------------------------------------------------------------------------------------------------------------
    # FIRST LOOP ITERATION; PREPROCESSING / ABSOLUTE MATCHING
    # ------------------------------------------------------------------------------------------------------------------

    def first_loop_iteration(self, compute_thumbnails: bool = True, compute_hash: bool = False, amount: int = 4,
                             cpu_proc: int = None):
        """
        Perform the preprocessing step. I.e. compute hashes, get image sizes, resize the images and store the
        thumbnails.

        ----------------------------------------------------------------------------------------------------------------

        Hashing:
        After the image has been resized, the bits of each r, g and b value are shifted by the amount specified in the
        amount parameter. If the amount is greater than 0, the bytes are right shifted, if the amount is smaller than 0,
        the pixels are left shifted.

        ----------------------------------------------------------------------------------------------------------------

        The program doesn't support hdr image formats and only allocates one byte per channel per pixel. Consequently
        10bit images for example are not supported. They are probably down-converted. # TODO Verify!!!


        :param compute_thumbnails: Resize images and store them temporarily
        :param compute_hash: Compute hashes of the image
        :param amount: shift amount before hash
        :param cpu_proc: number of cpu processes. Default number of system cores.
        :return:
        """
        # Writing the arguments to config
        self.config.state = "first_loop_in_progress"
        self.config.fl_compute_thumbnails = compute_thumbnails
        self.config.fl_compute_hash = compute_hash
        self.config.fl_shift_amount = amount
        self.config.fl_cpu_proc = cpu_proc
        self.config.write_to_file()

        # Reset the marked files in any case.
        self.logger.debug("Reset as in progress marked files")
        self.db.reset_first_loop_mark()

        self.config.write_to_file()
        # INFO: Since the database marks files that are

        # Short circuit if there are no images in the database.
        if not self.config.enough_images_to_compare:
            self.logger.debug("No images in database, aborting.")
            return

        if self.config.fl_cpu_proc is None:
            self.config.fl_cpu_proc = mp.cpu_count()

        # store thumbnails if possible.
        if compute_hash:
            if amount == 0:
                self.logger.warning("amount 0, only EXACT duplicates are detected like this.")

            if amount > 7 or amount < -7:
                raise ValueError("amount my only be in range [-7, 7]")

        # thumbnail are required to exist for both.
        if compute_thumbnails or compute_hash:
            self.check_create_thumbnail_dir()

        # reset handles and create queues.
        self.cpu_handles = []
        self.gpu_handles = []

        self.first_loop_in =  mp.Queue(self.config.max_queue_size) if self.db.thread_safe else mp.Queue()
        self.first_loop_out = mp.Queue(self.config.max_queue_size) if self.db.thread_safe else mp.Queue()

        # var for following while loop:
        run = True

        # prefill loop
        for i in range(self.config.fl_cpu_proc):
            arg = self.generate_first_loop_obj()

            # stop if there's nothing left to do.
            if arg is None:
                self.logger.info("Less images than processes, no continuous euqneueing.")
                run = False
                break

            self.first_loop_in.put(arg.to_json())
            self.config.fl_inserted_counter += 1

        v = self.verbose
        self.loop_run = True

        # start processes for cpu
        for i in range(self.config.fl_cpu_proc):
            p = mp.Process(target=parallel_resize, args=(self.first_loop_in, self.first_loop_out, i, False, v))
            p.start()
            self.cpu_handles.append(p)

        if self.db.thread_safe and self.config.fl_use_workers:
            self.__thread_safe_first_loop(run=run)
            return

        self.__non_thread_safe_first_loop(run=run)

        assert self.first_loop_out.empty(), f"Result queue is not empty after all processes have been killed.\n " \
                                            f"Remaining: {self.first_loop_out.qsize()}"
        # only update the config if the process wasn't terminated by a sigint.
        if self.loop_run:
            self.config.state = "first_loop_done"
            self.logger.info("All Images have been preprocessed.")
        else:
            self.logger.info("Successfully shutting down first loop.")
        self.config.write_to_file()
        self.loop_run = False

    def __thread_safe_first_loop(self, run: bool):
        """
        Contains the main loop of the first loop iteration with some initialisations that are specific to the
        thread_safe implementation.

        :param run: if there's images in the database that have not been enqueued.
        :return:
        """
        self.db.commit()

        self.en_com_1, en_com_2 = mp.Pipe()
        self.de_com_1, de_com_2 = mp.Pipe()

        enqueue_worker = None
        if run:
            enqueue_worker = mp.Process(target=first_loop_enqueue_worker,
                                        args=(self.first_loop_in, en_com_2, self.config.export_task_dict(),
                                              self.db.create_config_dump()))
            enqueue_worker.start()

        dequeue_worker = mp.Process(target=first_loop_dequeue_worker,
                                    args=(self.first_loop_out, de_com_2, self.config.export_task_dict(),
                                          self.db.create_config_dump()))
        dequeue_worker.start()

        self.en_com_1: con.Connection
        self.de_com_1: con.Connection

        if run:
            while enqueue_worker.is_alive() and self.loop_run:
                # Handling communications.
                if self.en_com_1.poll(timeout = 0.01):
                    self.logger.info(self.en_com_1.recv())

                if self.de_com_1.poll(timeout= 0.01):
                    self.logger.info(self.de_com_1.recv())

                time.sleep(0.1)

            enqueue_worker.join()

        # Joining.
        if not( run and self.loop_run):
            self.send_termination_signal(first_loop=True)

        for i in range(6000):
            if self.de_com_1.poll(timeout= 0.01):
                self.logger.info(self.de_com_1.recv())

            _, _, _, all_exited = self.check_children(gpu=False, cpu=True)
            if all_exited:
                break

        self.join_all_children()

        # waiting for dequeue_worker
        while dequeue_worker.is_alive() and self.loop_run:
            if self.de_com_1.poll(timeout= 0.01):
                self.logger.info(self.de_com_1.recv())

        dequeue_worker.join()
        self.en_com_1 = None
        self.de_com_1 = None

    def __non_thread_safe_first_loop(self, run: bool):
        """
        The main stage of the first loop. Starting the child processes and managing those and having the main thread
        taking care of enqueueing and dequeue the tasks and results.

        :param run: boolean if the continuous enqueue and dequeue loop needs to run.
        :return:
        """
        # turn main loop into handler and perform monitoring of the threads.
        none_counter = 0
        timeout = 0
        exit_count = 0

        # handle the running state of the loop
        while run and self.loop_run:
            if self.config.fl_inserted_counter % 100 == 0:
                self.logger.info(f"Inserted {self.config.fl_inserted_counter} images.")

            proc_suc, proc_exit = self.handle_result_of_first_loop(self.first_loop_out)
            exit_count += int(proc_exit)
            if proc_suc:
                arg = self.generate_first_loop_obj()

                # if there's no task left, stop the loop.
                if arg is None:
                    none_counter += 1
                    self.first_loop_in.put(None)

                else:
                    self.first_loop_in.put(arg.to_json())
                    self.config.fl_inserted_counter += 1
                    timeout = 0
            else:
                timeout += 1

            # if this point is reached, all processes should be done and the queues empty.
            if none_counter >= self.config.fl_cpu_proc:
                run = False

            # at this point we should have been idling for 60s
            if timeout > 5:
                self.logger.info("Timeout reached, stopping.")
                run = False

            if exit_count == self.config.fl_cpu_proc:
                self.logger.info("All processes exited - stopping.")
                run = False

        self.send_termination_signal(first_loop=True)
        self.logger.debug("Termination signal sent")

        counter = 0
        # try to handle any remaining results that are in the queue.
        while counter < 5:
            proc_suc, proc_exit = self.handle_result_of_first_loop(self.first_loop_out)
            exit_count += int(proc_exit)

            if not (proc_suc or proc_exit):
                counter += 1
                self.logger.debug("Timeout while dequeue")
                continue

            if exit_count == self.config.fl_cpu_proc:
                break

            counter = 0

        self.join_all_children()

    # ==================================================================================================================
    # SECOND LOOP ITERATION / DIFFERENCE RATING
    # ==================================================================================================================

    def second_loop_iteration(self, only_matching_aspect: bool = False, only_matching_hash: bool = False,
                              make_diff_plots: bool = False, similarity_threshold: Union[int, float] = 200.0, gpu_proc: int = 0,
                              cpu_proc: int = None, diff_location: str = None):
        """
        Similarity old values: high - 0.15, medium 200, low 1000

        :param only_matching_aspect: The images must match precisely in their size (in px)
        :param only_matching_hash: The images must have at least one matching hash.
        :param make_diff_plots: If the images which are duplicates should be plotted.
        :param similarity_threshold: The mean square average between pictures for them to be considered identical.
        :param gpu_proc: number of gpu processes. (Currently not implemented)
        :param cpu_proc: number of cpu processes. Default number of cpus on the system.
        :param diff_location: Where the plots should be stored (needs to be provided if make_diff_plots is true)
        :return:
        """
        # TODO check the number of images with self.db.get_dir_count() -> set the less optimized flag there and then
        #   make the adjustment fro there.
        # Writing to config.
        self.config.state = "second_loop_in_progress"
        self.config.sl_gpu_proc = gpu_proc
        self.config.sl_cpu_proc = cpu_proc
        self.config.sl_matching_aspect = only_matching_aspect
        self.config.sl_make_diff_plots = make_diff_plots
        self.config.sl_matching_hash = only_matching_hash
        self.config.similarity_threshold = float(similarity_threshold)
        self.config.state = "second_loop_in_progress"

        # Short circuit if there are no images in the database.
        if not self.config.enough_images_to_compare:
            self.logger.debug("No images in database, aborting.")
            return

        assert gpu_proc >= 0, "Number of GPU Processes needs to be greater than zero"
        if self.config.sl_cpu_proc is None:
            self.config.sl_cpu_proc = mp.cpu_count()

        assert self.config.sl_cpu_proc >= 1, "Number of GPU Processes needs to be greater than zero"

        self.config.sl_has_thumb = self.db.test_thumb_existence()

        if make_diff_plots:
            # diff_location is stored in config in this function.
            self.create_plot_dir(diff_location=diff_location)

        self.config.write_to_file()

        self.__sl_determine_algo()

        self.cpu_handles = []
        self.gpu_handles = []

        # create queues
        self.second_loop_out = mp.Queue()

        # Creating second_loop_in -> depending on less_optimized and thread_safe_db
        if self.config.less_optimized:
            if self.db.thread_safe:
                self.second_loop_in = mp.Queue(self.config.max_queue_size *
                                               (self.config.sl_cpu_proc + self.config.sl_gpu_proc))
            else:
                self.second_loop_in = mp.Queue()

        else:
            if self.db.thread_safe:
                self.second_loop_in = [mp.Queue(self.config.max_queue_size)
                                       for _ in range(self.config.sl_gpu_proc + self.config.sl_cpu_proc)]
            else:
                self.second_loop_in = [mp.Queue()
                                       for _ in range(self.config.sl_gpu_proc + self.config.sl_cpu_proc)]

        child_args = [(self.second_loop_in if self.config.less_optimized else self.second_loop_in[i],
                       self.second_loop_out, i, i >= self.config.sl_cpu_proc ,
                       False,
                       False,
                       self.verbose)
                          for i in range(self.config.sl_gpu_proc + self.config.sl_cpu_proc)]

        # prefill
        if self.config.sl_queue_status is None:
            self.__init_queues()

        # starting all processes
        for i in range(self.config.sl_cpu_proc):
            p = mp.Process(target=parallel_compare, args=child_args[i])
            p.start()
            self.cpu_handles.append(p)

        for i in range(self.config.sl_cpu_proc, self.config.sl_cpu_proc + self.config.sl_gpu_proc):
            p = mp.Process(target=parallel_compare, args=child_args[i])
            p.start()
            self.gpu_handles.append(p)

        if self.db.thread_safe and self.config.sl_use_workers:
            self.__thread_safe_second_loop()
            return

        self.__non_thread_safe_second_loop()

    def __thread_safe_second_loop(self):
        """
        Thread safe implementation of the main loop of the second loop iteration. Thread safe specific inits and
        termination sequences.

        :return:
        """
        self.db.commit()
        self.en_com_1, en_com_2 = mp.Pipe()
        self.de_com_1, de_com_2 = mp.Pipe()
        enqueue_thread = None
        self.loop_run = True

        if self.__require_queue_refill():
            enqueue_thread = mp.Process(target=second_loop_enqueue_worker,
                                        args=(self.second_loop_in, en_com_2, self.config.export_task_dict(),
                                              self.db.create_config_dump()))
            enqueue_thread.start()

        dequeue_thread = mp.Process(target=second_loop_dequeue_worker,
                                    args=(self.second_loop_out, de_com_2,
                                          self.config.export_task_dict(), self.db.create_config_dump()))
        dequeue_thread.start()

        while enqueue_thread is not None and enqueue_thread.is_alive() and self.loop_run:
            # Handling communications.
            if self.en_com_1.poll(timeout=0.01):
                self.logger.info(self.en_com_1.recv())

            if self.de_com_1.poll(timeout=0.01):
                self.logger.info(self.de_com_1.recv())

        if enqueue_thread is not None:
            enqueue_thread.join()

        if not self.loop_run or enqueue_thread is None:
            self.send_termination_signal(first_loop=False)

        # emptying pipe
        while self.en_com_1.poll(timeout=0.01) and self.loop_run:
            self.logger.info(self.en_com_1.recv())

        # waiting for dequeue_worker
        while dequeue_thread.is_alive() and self.loop_run:
            # polling the queues:
            if self.de_com_1.poll(timeout=0.01):
                self.logger.info(self.de_com_1.recv())

        for i in range(6000):
            if self.de_com_1.poll(timeout=0.01):
                self.logger.info(self.de_com_1.recv())

            _, _, _, all_exited = self.check_children(gpu=self.config.sl_gpu_proc > 0, cpu=self.config.sl_cpu_proc > 0)
            if all_exited:
                break

        if not self.loop_run:
            self.send_termination_signal(first_loop=False)
        self.join_all_children()

        dequeue_thread.join()
        assert self.first_loop_out.empty(), f"Result queue is not empty after all processes have been killed.\n " \
                                            f"Remaining: {self.first_loop_out.qsize()}"

        self.en_com_1 = None
        self.de_com_1 = None
        if self.loop_run:
            self.config.state = "second_loop_done"
            self.logger.info("Data should be committed")
        else:
            self.logger.info("Successfully shutting down second loop.")
        self.config.write_to_file()
        self.loop_run = False

    def __non_thread_safe_second_loop(self):
        """
        None thread safe implementation of the main loop of the second loop iteration. Thread safe specific inits and
        termination sequences.
        
        :return:
        """
        # check if we need multiple iterations of the main loop.
        done = self.__require_queue_refill()
        count = 0
        timeout = 0
        none_count = 0
        self.loop_run = True

        # update everything
        while done and self.loop_run:
            # update the queues and store if there are more tasks to process
            current_inserted, current_count, current_none_count = self.update_queues()
            count += current_count
            none_count += current_none_count
            self.logger.info(f"Number of Processed Images: {count:,}".replace(",", "'"))

            # We have no more images to enqueue
            if current_inserted == 0 or none_count >= self.config.sl_gpu_proc + self.config.sl_cpu_proc:
                self.send_termination_signal(first_loop=False)
                self.logger.debug("End of images reached.")
                done = False

            if current_count == 0:
                timeout += 1
                self.logger.debug("Dequeued 0 elements")
                time.sleep(1)

                if timeout > 5:
                    done = False
            else:
                timeout = 0

            self.handle_results_second_queue()
            # exit the while loop if all children have exited.
            _, _, _, all_exited = self.check_children(cpu=self.config.sl_cpu_proc > 0, gpu=self.config.sl_gpu_proc > 0)
            if all_exited:
                self.logger.debug("All Exited")
                done = False

        if not self.loop_run:
            self.send_termination_signal(first_loop=False)

        # check if it was the children's fault
        _, all_errored, _, _ = self.check_children(cpu=self.config.sl_cpu_proc > 0, gpu=self.config.sl_gpu_proc > 0)

        if all_errored:
            raise RuntimeError("All child processes exited with an Error")

        self.join_all_children()
        self.logger.debug("All child processes terminated")

        timeout = 0
        while timeout < 5:
            # handle last results:
            if (0, 0) == self.handle_results_second_queue():
                timeout += 1
                continue

            timeout = 0

        # check if the tasks were empty.
        assert (0, 0) ==  self.handle_results_second_queue(), "Existed without having run out of tasks and without all " \
                                                       "processes having stopped."

        self.loop_run = False
        self.db.commit()
        if self.loop_run:
            self.config.state = "second_loop_done"
            self.logger.debug("Data should be committed")
        else:
            self.logger.info("Successfully shutting down second loop.")
        self.config.write_to_file()

    def __sl_determine_algo(self):
        """
        Determine if we use the optimized or non-optimized algorithm. => Important for layout of queues etc.
        Sets *config.sl_base_a* and *config.less_optimized*
        :return:
        """
        proc_count = self.config.sl_cpu_proc + self.config.sl_gpu_proc

        dir_a_count = self.db.get_dir_count(dir_a=True)
        dir_b_count = dir_a_count

        if self.config.has_dir_b:
            dir_b_count = self.db.get_dir_count(dir_a=False)

        if dir_a_count >= proc_count:
            self.config.sl_base_a = True
            return

        # dir_a has less than processes images
        if self.config.has_dir_b and dir_b_count >= proc_count:
            self.config.sl_base_a = False
            return

        # We have fewer images than processes in both folders. => Using less optimized approach
        self.config.less_optimized = True

    def __require_queue_refill(self):
        """
        Check if the queues need to be continuously refilled as in not all comparisons have been scheduled.
        :return: true - more comparisons need to be scheduled.
        """
        done = True
        a_count = self.db.get_dir_count(dir_a=True)
        b_count = self.db.get_dir_count(dir_a=False)

        if self.config.has_dir_b:
            comps = a_count * b_count

            if comps < (self.config.sl_cpu_proc + self.config.sl_gpu_proc) * 100:
                self.send_termination_signal(first_loop=False)
                done = False
                self.logger.info("Less comparisons than available space. Not performing continuous enqueue.")

        else:
            comps = a_count * (a_count - 1) / 2
            if comps < (self.config.sl_cpu_proc + self.config.sl_gpu_proc) * 100:
                self.send_termination_signal(first_loop=False)
                done = False
                self.logger.info("Less comparisons than available space. Not performing continuous enqueue.")
        return done

    def create_plot_dir(self, diff_location: str):
        """
        Verifies the provided directory, creates if it doesn't exist.

        :param diff_location: path to plot where the plots are to be saved
        :return:
        """
        if diff_location is None:
            raise ValueError("If plots are to be generated, an output folder needs to be specified.")
        if not os.path.isdir(diff_location):
            raise ValueError("Plot location doesn't specify a valid directory path")

        if not os.path.exists(diff_location):
            os.makedirs(diff_location)

        self.config.sl_plot_output_dir = diff_location

    def update_queues(self):
        enqueued, none_count = self.sl_refill_queues(in_queue=self.second_loop_in)
        dequeued, _ = self.handle_results_second_queue(enqueued)
        return enqueued, dequeued, none_count

    def __init_queues(self):
        """
        Initialize the state describing variables as well as the queues for the second loop.
        :return:
        """
        processes = self.config.sl_cpu_proc + self.config.sl_gpu_proc
        # we are using less optimized, so we are going straight for the not optimized algorithm.
        if self.config.less_optimized:
            first_key = self.db.fetch_many_after_key(directory_a=True, starting=None, count=1)
            self.config.sl_queue_status = {"fix_key": first_key[0]["key"], "shift_key": None, "done": False,
                                           "none_count": 0}

            # Only on dir to itself - only upper matrix to be computed.
            if not self.config.has_dir_b:
                self.config.sl_queue_status["shift_key"] = first_key[0]["key"]

            return

        # from a fetch the first set of images
        if self.config.sl_base_a:
            rows = self.db.fetch_many_after_key(directory_a=True, count=processes)
        else:
            rows = self.db.fetch_many_after_key(directory_a=False, count=processes)

        # populating the files of the second loop.
        self.config.sl_queue_status = []

        if self.config.sl_base_a:
            for row in rows:
                # The last_key can be set if we have second_loop_base_a and no dir_b because we're looking only at an
                # upper triangular matrix of the Cartesian product of the elements of the image itself.
                temp = {"row_a": row, "last_key": None if self.config.has_dir_b else row["key"]}

                self.config.sl_queue_status.append(temp)
        else:
            for row in rows:
                temp = {"row_b": row, "last_key": None}

                self.config.sl_queue_status.append(temp)

        self._refill_queues_optimized_base(queue_list=self.second_loop_in)

    def handle_results_second_queue(self, max_number: int = None) -> Tuple[int, int]:
        """
        Dequeue up to max_number of entries of the result queue of the second loop and insert the results into the
        database.

        :param max_number: maximum number of elements to dequeue, if None, dequeue until queue is empty.
        :return: -> Number actually dequeued elements
        """
        # TODO test for existence (for stop recovery)
        number_dequeues = 0
        number_exited = 0
        if max_number is None:
            while True:
                proc_suc, proc_exit = self.process_one_second_result(out_queue=self.second_loop_out)
                if not proc_suc and not proc_exit:
                    return number_dequeues, number_exited

                number_dequeues += int(proc_suc)
                number_exited += int(proc_exit)

        # we have a max_number
        for i in range(max_number):
            proc_suc, proc_exit = self.process_one_second_result(out_queue=self.second_loop_out)
            number_dequeues += int(proc_suc)
            number_exited += int(proc_exit)

            if not proc_suc and not proc_exit:
                return number_dequeues, number_exited

        return number_dequeues, number_exited

    def check_children(self, gpu: bool = False, cpu: bool = False):
        """
        Iterator over specified child processes and verify if any or all exited and produced an error.

        If nothing is selected, teh default is ,
        all_error is true,
        all_exited is true,
        error is false and
        exited is false.

        :param gpu: Test the gpu processes
        :param cpu: Test the cpu processes
        :return: error, all_error, exited, all_exited
        """
        # error, all_error, exited, all_exited
        error = False
        all_error = True
        exited = False
        all_exited = True

        # info, results can be fetched twice
        # check on the gpu tasks
        if gpu:
            error, all_error, exited, all_exited = self.check_processes(self.gpu_handles)

        if cpu:
            er, a_er, ex, a_ex = self.check_processes(self.cpu_handles)
            error = error or er
            all_error = all_error and a_er
            exited = exited or ex
            all_exited = all_exited and a_ex

        return error, all_error, exited, all_exited

    def check_processes(self, processes: List[mp.Process]) -> Tuple[bool, bool, bool, bool]:
        """
        Given a list of Futures, check for errors and if they are done.

        :param processes: List of futures to check
        :return: exited, all_exited
        """
        exited = False
        all_exited = True
        error = False
        all_error = False

        for p in processes:
            # if it is running, it has not exited and not errored
            if not p.is_alive():
                e = p.exitcode

                if e is not None:
                    if e != 0:
                        error = True
                    else:
                        all_error = False

                else:
                    self.logger.warning("process is not alive but no exit code available")

            else:
                all_error = False
                all_exited = False

        return error, all_error, exited, all_exited

    # ==================================================================================================================
    # DATA RETRIEVAL FUNCTIONS
    # ==================================================================================================================

    def get_duplicates(self, similarity: float = None, dif_based: bool = True):
        """
        Builds the duplicates clusters. The function returns the

        :param similarity: amount that the dif amount needs to lay below.
        :param dif_based: if the relative difference should be used or hash based matching should be done.
        :return:
        """
        if not self.config.enough_images_to_compare:
            return {}, []

        if not dif_based:
            raise NotImplementedError("hash_based is in todos.")
        clusters = self.build_loose_duplicate_cluster(similarity)
        return self.find_best_image(clusters)

    def spawn_duplicate_pair_worker(self, queue_size: int = 1000, start_id: int = None, threshold: float = 200) \
            -> Tuple[mp.Queue, th.Thread]:
        """
        Function creates a worker thread which continuously enqueues dicts of each matching pair into the returned
        transfer queue.

        The queue will contain dicts with the following keys:
        key: id of that dif pair in the dif table. (can be provided as start id)
        key_a: key of the first file in the directory table
        key_b: key of the second file in the directory table
        b_dir_b: if the second file is in the b directory or the a directory
        path_X: path to file a or b
        filename_X: filename of file a or b
        px_X: horizontal pixel count of file a or b
        py_X: vertical pixel count of file a or b

        :param queue_size: max_size the queue can reach
        :param start_id: from which key the thread should start adding the matching pairs
                (in case the process got stopped)
        :param threshold: difference value below something must lay for it to be considered to be a duplicate.
        :return: queue containing dicts of the matching pairs, thread object that is filling the queue.
        """
        transfer_queue = mp.Queue(maxsize=queue_size)
        process = th.Thread(target=self.continuous_dif_pair_dequeue_worker, args=(transfer_queue, start_id, threshold))
        process.start()
        return transfer_queue, process

    def continuous_dif_pair_dequeue_worker(self, out_queue: mp.Queue, start: int = None, threshold: float = 200):
        """
        Worker function for get_duplicates. Performs the fetching from db, wrapping in dicts and putting in queue.

        The queue will contain dicts with the following keys:
        key: id of that dif pair in the dif table. (can be provided as start id)
        key_a: key of the first file in the directory table
        key_b: key of the second file in the directory table
        b_dir_b: if the second file is in the b directory or the a directory
        path_X: path to file a or b
        filename_X: filename of file a or b
        px_X: horizontal pixel count of file a or b
        py_X: vertical pixel count of file a or b

        :param out_queue: queue to put the wrapped results into
        :param start: starting key in dif table
        :param threshold: measurement under which the difference must lay.
        :return: None
        """
        # get initial number of pairs and make sure they are not empty.
        pairs = self.db.get_many_pairs(threshold=threshold, start_key=start)
        if len(pairs) == 0:
            return

        # Perform with JOIN: TODO
        # SELECT * FROM dif_table JOIN directory d on dif_table.key_a = d.key JOIN
        # directory dd on dif_table.key_b = dd.key;
        while True:
            # process each pair and put it in a queue.
            for p in pairs:
                key_a = self.db.fetch_row_of_key(key=p["key_a"])
                key_b = self.db.fetch_row_of_key(key=p["key_b"])
                p["path_a"] = key_a["path_a"]
                p["filename_a"] = key_a["filename_a"]
                p["px_a"] = key_a["px_a"]
                p["py_a"] = key_a["py_a"]
                p["path_b"] = key_b["path_b"]
                p["filename_b"] = key_b["filename_b"]
                p["px_b"] = key_b["px_b"]
                p["py_b"] = key_b["py_b"]
                del p["dif"]
                del p["error"]
                del p["success"]

                out_queue.put(p, block=True)

            last_key = pairs[-1]["key"]
            pairs = self.db.get_many_pairs(threshold=threshold, start_key=last_key)

            if len(pairs) == 0:
                return

    def print_preprocessing_errors(self):
        """
        Function fetches all errors that were encountered during the preprocessing phase and  prints them to the
        console.

        :return:
        """
        last_key = None

        # get the errors as long as there are any
        while True:
            results = self.db.get_many_preprocessing_errors(start_key=last_key, count=1000)

            if len(results) == 0:
                break

            for r in results:
                path = r['path']
                error = r['error']
                print(f"File {path} encountered error:\n{error}")

            last_key = results[-1]['key']

        print("-"*120)

    def print_compare_errors(self):
        """
        Function fetches all errors that were encountered during the comparison of the files and prints them to the
        console.

        :return:
        """
        errors = True
        last_key = None

        while errors:
            results = self.db.get_many_comparison_errors(start_key=last_key)

            if len(results) == 0:
                errors = False

            for r in results:
                path_a = r['a_path']
                path_b = r['b_path']
                error = r['error']
                print(f"Comparison of Files {path_a} and {path_b} encountered error:\n{error}")

            last_key = results[-1]['dif_key']

        print("-"*120)

    def spawn_duplicate_error_worker(self):
        """
        TODO Docstring
        :return:
        """
        raise NotImplementedError("Need to implement that one")

    def spawn_preprocessing_error_worker(self):
        """
        TODO Docstring
        :return:
        """
        raise NotImplementedError("Need to implement that one")

    def continuous_duplicate_error_worker(self):
        """
        TODO docstring
        :return:
        """
        raise NotImplementedError("Need to implement that one")

    def continuous_preprocessing_error_worker(self):
        """
        TODO docstring
        :return:
        """
        raise NotImplementedError("Need to implement that one")

    def build_loose_duplicate_cluster(self, similarity: float = None):
        """
        Function generates a list of dicts containing duplicates. Each dict in the list satisfies that there exists at
        least **one** path between each two images. It is **not** guaranteed that within a cluster each pair of images
        matches the similarity threshold.

        This function is implemented in **RAM** only. If the dataset to deduplicate is too large, it is possible that
        this function fails due to insufficient memory. A Database driven solution might exist in the future.

        Alternatively, there's also the functionality to create a process which reads out the database and fills a
        queue. That way each pair of duplicates images can be processed separately by an external application.
        See *spawn_duplicate_worker*

        :param similarity: The average difference between the pixels that should be allowed. If left empty, it reuses
        the value from the call to second_loop_iteration
        :return:
        """
        self.db.commit()
        if similarity is None:
            similarity = self.config.similarity_threshold

        if similarity <= 0:
            raise ValueError("No Similarity provided and / or similarity_threshold from second loop not usable.")

        all_duplicate_pairs = self.db.get_all_matching_pairs(similarity)

        clusters: Dict[str, list] = {}
        cluster_id: dict = {}

        next_id = 0
        count = 0
        for row in all_duplicate_pairs:
            if count % 100 == 0:
                if self.verbose:
                    print(f"Done with {count}", end="\r", flush=True)
            count += 1

            # get the data from the rows
            key_a = row[1]
            key_b = row[2]

            assert key_a != key_b, "Key A and Key B are the same, bug in scheduling."

            # get the cluster for the keys
            cluster_id_a = cluster_id.get(key_a)
            cluster_id_b = cluster_id.get(key_b)

            next_id = self.process_pair(cluster_id_a, cluster_id_b, next_id, clusters, cluster_id,
                                        key_a, key_b)

        return clusters

    def process_pair(self, cluster_id_a: str, cluster_id_b: str, next_id: int, clusters: Dict[str, list],
                     cluster_id: dict, graph_key_a: str, graph_key_b: str):
        """
        Given a pair of graph_keys and cluster_ids, update the clusters and the cluster_ids dict accordingly.

        :param cluster_id_a: The id of the cluster in which graph_key_a is.
        :param cluster_id_b: The id of the cluster in which graph_key_b is.
        :param next_id: The next cluster_id that should be used if a new one was to be created
        :param clusters: Dict containing the clusters. [cluster_id, list of graph_keys]
        :param cluster_id: Dict containing the cluster_ids of every graph_key
        :param graph_key_a: The key of image_a in correct format
        :param graph_key_b: The key of image_b in correct format
        :return: the next id.
        """

        # No key is in a cluster, creating a new one.
        if cluster_id_a is None and cluster_id_b is None:
            new_cluster_id = str(next_id)

            clusters[new_cluster_id] = [graph_key_a, graph_key_b]
            cluster_id[graph_key_a] = new_cluster_id
            cluster_id[graph_key_b] = new_cluster_id
            return next_id + 1

        # We add image_a to the cluster in which image_b is located.
        elif cluster_id_a is None and cluster_id_b is not None:
            clusters[cluster_id_b].append(graph_key_a)
            cluster_id[graph_key_a] = cluster_id_b
            return next_id

        # We add image_b to the cluster in which image_a is located
        elif cluster_id_a is not None and cluster_id_b is None:
            clusters[cluster_id_a].append(graph_key_b)
            cluster_id[graph_key_b] = cluster_id_a
            return next_id

        # We have two clusters that need to be merged. or a duplicate row
        else:
            if cluster_id_a == cluster_id_b:
                return next_id

            # We merge the two clusters into one.
            else:
                self.logger.debug("Merging clusters")
                # Select the smaller cluster to merge it into the larger cluster
                if len(clusters[cluster_id_a]) < len(clusters[cluster_id_b]):

                    # changing the cluster id
                    for graph_key in clusters[cluster_id_a]:
                        cluster_id[graph_key] = cluster_id_b

                    # copy the stuff over.
                    clusters[cluster_id_b].extend(clusters[cluster_id_a])

                    # dropping cluster_a
                    del clusters[cluster_id_a]

                else:
                    # changing the cluster id
                    for graph_key in clusters[cluster_id_b]:
                        cluster_id[graph_key] = cluster_id_a

                    # copy the stuff over.
                    clusters[cluster_id_a].extend(clusters[cluster_id_b])

                    # dropping cluster_a
                    del clusters[cluster_id_b]
                return next_id

    def find_best_image(self, cluster: Dict[str, list], comparator: FunctionType = None):
        """
        Given a dict of clusters, go through the clusters and determine the best image based on a comparator function.

        :param comparator: function to use to determine best image in set of duplicates.
        :param cluster: dict containing lists.
        :return: dict containing the diplicate clusters and a list of all lower quality image filepaths.
        """
        fp_list = []
        for cluster_id, images in cluster.items():
            if len(images) > 1000:
                self.logger.debug("Excessive amount of duplicates found.")

            if len(images) == 0:
                self.logger.warning("Found empty images list")

            filepaths = []

            for img_key in images:
                info = self.db.fetch_row_of_key(key=img_key)
                filepaths.append(info["path"])

            fp_list.append((filepaths, comparator))

        # create an executor
        ppe = ProcessPoolExecutor()
        results = ppe.map(find_best_image, fp_list)

        # process results
        lower_quality = []
        output = {}
        for result in results:
            # unpacking tuple
            res_dict, dups = result

            # updating global info.
            lower_quality.extend(dups)
            res_dict["duplicates"] = dups
            output[datetime.datetime.utcnow().timestamp()] = res_dict

        return output, lower_quality

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def verbose(self):
        return self.config.verbose

    @verbose.setter
    def verbose(self, value):
        if type(value) is not bool:
            raise TypeError("Verbose is a boolean")

        self.config.verbose = value

        # update the logging level.
        if self.config.verbose:
            self.stream_handler.setLevel(logging.INFO)
        else:
            self.stream_handler.setLevel(logging.WARNING)

    def prepare_logging(self, console_level: int = logging.DEBUG, debug: bool = False):
        """
        Set's up logging for the class.

        :param console_level: log level of the console. use logging.LEVEL for this.
        :param debug: store the console log also inside a separate file.
        :return:
        """
        self.logger = logging.getLogger("fast_diff_py")

        # reconnecting handlers if previous handlers exist.
        if self.logger.hasHandlers():
            self.logger.debug("Logger has previous handlers, reconnecting them, assuming default config.")
            for handler in self.logger.handlers:
                if type(handler) is logging.StreamHandler:

                    # Follows from type checking
                    handler: logging.StreamHandler
                    self.stream_handler = handler
                if type(handler) is logging.FileHandler:

                    # Follows from Type checking
                    handler: logging.FileHandler
                    if handler.level is logging.WARNING:
                        self.file_handler = handler
                    else:
                        self.debug_logger = handler
            return

        # get location for the logs
        fp = os.path.abspath(os.path.dirname(__file__))

        # create two File handlers one for logging directly to file one for logging to Console
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.file_handler = logging.FileHandler(os.path.join(fp, "execution.log"))

        # create Formatter t o format the logging messages in the console and in the file
        console_formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # add the formatters to the respective Handlers
        self.stream_handler.setFormatter(console_formatter)
        self.file_handler.setFormatter(file_formatter)

        # Set the logging level to the Handlers
        self.stream_handler.setLevel(console_level)
        self.file_handler.setLevel(logging.WARNING)

        # Add the logging Handlers to the logger instance
        self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(self.file_handler)

        # In case a Debug log is desired create another Handler, add the file formatter and add the Handler to the
        # logger
        if debug:
            self.add_debug_logger(file_formatter, fp)

        # We do not want to pollute the information of the above loggers, so we don't propagate
        # We want our logger to emmit every message to all handlers, so we set it to DEBUG.
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)

    def add_debug_logger(self, file_formatter: logging.Formatter, out_dir: str = None):
        """
        Function gets called if prepare_logging has debug set. It can be called alternatively later on during code
        execution if one wants to get a preciser information about what is going on.

        There can only be one debug logger at a time. If this function is called twice, the old logger will be removed
        and the new one will be added. THIS MAY OVERWRITE THE DEBUG FILE IF THE __out_dir__ IS NOT SET!!!

        :param file_formatter: the formatter with which to create the logs.
        :param out_dir: Directory where the logs should be saved
        :return:
        """

        if out_dir is None:
            out_dir = os.path.abspath(os.path.dirname(__file__))

        if self.debug_logger is None:
            self.debug_logger = logging.FileHandler(os.path.join(out_dir, "debug_execution.log"))
            self.debug_logger.setFormatter(file_formatter)
            self.debug_logger.setLevel(logging.DEBUG)
            self.logger.addHandler(self.debug_logger)

        # remove eventually preexisting logger
        else:
            self.logger.removeHandler(self.debug_logger)
            self.add_debug_logger(file_formatter, out_dir)
