from types import FunctionType
from fast_diff_py.datatransfer import *
import os
from typing import Tuple, Union
import cv2
from matplotlib import pyplot as plt
import skimage
from fast_diff_py.utils import *


# sample for the idiot I am.
# import matplotlib.pyplot as plt
# import numpy as np
# import cv2
#
# # Some example data to display
# x = np.linspace(0, 2 * np.pi, 400)
# y = np.sin(x ** 2)
#
# fig, ax = plt.subplots()
# ax.plot(x, y)
# ax.set_title('A single plot')
# plt.show()
#
# fig, axs = plt.subplots(2, 2)
# fig.suptitle('Vertically stacked subplots')
# axs[0][0].plot(x, y)
# axs[1][0].plot(x, -y)
#
# im_a = "/home/alisot2000/Desktop/SAMPLE_MIRA/JOIN/20221206_014252.jpg"
# im_b = "/home/alisot2000/Desktop/SAMPLE_MIRA/JOIN/0C2E9779-8E7C-4044-B2D3-07C8F8650527.jpeg"
#
# im_a_mat = cv2.imdecode(np.fromfile(im_a, dtype=np.uint8), cv2.IMREAD_COLOR)
# im_b_mat = cv2.imdecode(np.fromfile(im_b, dtype=np.uint8), cv2.IMREAD_COLOR)
#
# axs[0][1].imshow(im_a_mat, cmap=plt.cm.gray)
# axs[1][1].imshow(im_b_mat, cmap=plt.cm.gray)
#
# plt.show()


class CPUImageProcessing:
    """
    This class Contains the functions to process a single image or a pari of images.

    The intent of this class is to be instantiated in the parallel processes running as slaves. It gets passed the
    arguments from the slave and then has the ability to reuse parts of the computation from before (say you have an
    all to all comparison, you can have one slave keep one image constant and iterate through the others.)

    The class needs to be aware of the availability of cuda / cupy and use it if indicated by the slave running the
    class.
    """
    # TODO Make class Cupy compatible
    identifier: int

    image_a_path: Union[str, None] = None
    image_b_path: Union[str, None] = None

    thumb_a_path: Union[str, None] = None
    thumb_b_path: Union[str, None] = None

    image_a_matrix: Union[np.ndarray, None] = None
    image_b_matrix: Union[np.ndarray, None] = None

    target_size_x: int = 64
    target_size_y: int = 64

    original_size_x: int = 0
    original_size_y: int = 0

    diff_0: float = 0
    diff_90: float = 0
    diff_180: float = 0
    diff_270: float = 0

    hash_0: str = ""
    hash_90: str = ""
    hash_180: str = ""
    hash_270: str = ""

    processing_args: Union[CompareImageArguments, None] = None
    preprocessing_args: Union[PreprocessArguments, None] = None
    last_args: Union[CompareImageArguments, PreprocessArguments] = None

    error: str = None

    compare_func = None

    def __init__(self, identifier: int, comp: FunctionType = None):
        """
        Identifier provided by the parent process. Used to identify the process in the console.

        Specification of comparison:
        Input: two np.ndarray of the same shape. (the images)
        Output: float value of the computed difference.

        :param identifier: process id (not pid)
        :param comp: comparison function to use. If none is provided, the default is used.
        """
        self.identifier = identifier
        if comp is not None:
            self.compare_func = comp
        else:
            self.compare_func = self.mse

    def reset(self):
        """
        Utility to reset the diff values.
        :return:
        """

        # Reset the class for further processing.
        self.image_a_path = None
        self.image_b_path = None

        self.thumb_a_path = None
        self.thumb_b_path = None

        self.image_a_matrix = None
        self.image_b_matrix = None

        self.target_size_x = 64
        self.target_size_y = 64

        self.original_size_x = 0
        self.original_size_y = 0

        self.diff_0 = 0
        self.diff_90 = 0
        self.diff_180 = 0
        self.diff_270 = 0

        self.hash_0 = ""
        self.hash_90 = ""
        self.hash_180 = ""
        self.hash_270 = ""

    @staticmethod
    def mse(image_a: np.ndarray, image_b: np.ndarray) -> float:
        """
        The mean squared error, which is the base for the other metrics.
        """
        difference = image_a.astype("float") - image_b.astype("float")
        sq_diff = np.square(difference)
        sum_diff = np.sum(sq_diff)
        px_count = image_a.shape[0] * image_a.shape[1]
        return sum_diff / px_count

    def update_preprocess_args(self, args: PreprocessArguments, load: bool = True):
        """
        Loads the PreprocessArguments and updates the class attributes accordingly.
        Also resets any previously occurred errors.

        :param args: arguments to fill into attributes
        :param load: if the image should be loaded after updating the args through the update function.
        :return:
        """
        self.preprocessing_args = args
        self.error = ""

        if self.last_args is CompareImageArguments:
            self.reset()

        if self.image_a_path != args.in_path:
            load = True
            self.image_a_matrix = None
            self.image_a_path = args.in_path
            self.thumb_a_path = args.out_path

        if self.target_size_x != args.size_x or self.target_size_y != args.size_y:
            load = True
            self.target_size_x = args.size_x
            self.target_size_y = args.size_y
            self.image_a_matrix = None

        if load:
            self.load_image(image_a=True, perform_resize=False)

    def create_error_preprocess_result(self):
        """
        Create an PreprocessResults object given the existence of an error

        :return:
        """
        return PreprocessResults.error_obj(in_path=self.preprocessing_args.in_path,
                                           out_path=self.preprocessing_args.out_path,
                                           error=self.error,
                                           key=self.preprocessing_args.key
                                           )

    def create_no_hash_preprocess_result(self):
        """
        Create a PreprocessResults object given no computed hashed to be returned

        :return:
        """
        return PreprocessResults.no_hash_init(in_path=self.preprocessing_args.in_path,
                                              out_path=self.preprocessing_args.out_path,
                                              original_x=self.original_size_x,
                                              original_y=self.original_size_y,
                                              key=self.preprocessing_args.key
                                              )

    def create_full_preprocess_result(self):
        """
        Create a fully populated preprocess results object.

        :return:
        """
        return PreprocessResults(
            in_path=self.preprocessing_args.in_path,
            out_path=self.preprocessing_args.out_path,
            success=True,
            error="<EMPTY>",
            original_x=self.original_size_x,
            original_y=self.original_size_y,
            hash_0=self.hash_0,
            hash_90=self.hash_90,
            hash_180=self.hash_180,
            hash_270=self.hash_270,
            key=self.preprocessing_args.key
        )

    def update_compare_args(self, args: CompareImageArguments):
        """
        Update the CompareImageArguments object and update the class variables so the computations can be performed.
        Also resets any previously occurred errors.

        :param args: new CompareImageArguments object to process
        :return:
        """
        self.processing_args = args
        self.error = ""
        load_a = False
        load_b = False

        # Reset the Class for further processing
        if self.last_args is PreprocessArguments:
            self.reset()

        # reload Image A if thumb or image has changed
        if self.image_a_path != args.img_a or self.thumb_a_path != args.thumb_a:
            self.image_a_path = args.img_a
            self.thumb_a_path = args.thumb_a
            self.image_a_matrix = None
            load_a = True

        # reload Image B if thumb or image has changed
        if self.image_b_path != args.img_b or self.thumb_b_path != args.thumb_b:
            self.image_b_path = args.img_b
            self.thumb_b_path = args.thumb_b
            self.image_b_matrix = None
            load_b = True

        if self.target_size_x != args.size_x or self.target_size_y != args.size_y:
            self.target_size_x = args.size_x
            self.target_size_y = args.size_y
            self.image_a_matrix = None
            self.image_b_matrix = None
            load_a = True
            load_b = True

        # load the images if the arguments change them.
        if load_a:
            self.load_image(True)
        if load_b:
            self.load_image(False)

    def load_image(self, image_a: bool = True, perform_resize: bool = True):
        """
        Load image from file_system

        :param image_a: if the image_a should be loaded or image_b
        :param perform_resize: automatically resize image if they don't match the size.
        :return:
        """
        source = "image_a" if image_a else "image_b"
        image_path = self.image_b_path
        thumbnail_path = self.thumb_b_path

        # load the image_a stuff if the image_a is set.
        if image_a:
            image_path = self.image_a_path
            thumbnail_path = self.thumb_a_path

        if thumbnail_path is not None and os.path.exists(thumbnail_path):
            result, err_str, rescale = self.__image_loader(thumbnail_path, f"{source} thumbnail")

            # The thumbnail size matches and no error occurred while loading it. Storing the result and returning.
            if not rescale and err_str == "":
                if image_a:
                    self.image_a_matrix = result
                else:
                    self.image_b_matrix = result
                return

            if err_str != "":
                print(f"{self.identifier: 02}: {err_str}")

        # At this point thumbnail loading failed or the thumbnail was not computed. Load the image and resize if given
        # by args.
        if not os.path.exists(image_path):
            # the main image is the last solution, and we will store the error and return immediately if the error is
            # found.
            self.error = f"Error {source} failed to load because the file does not exist."
            return

        # load the image and return immediately if an error occurred.
        result, err_str, rescale = self.__image_loader(image_path, f"{source} original")
        if err_str != "":
            self.error = err_str
            return

        # store image size
        self.original_size_y, self.original_size_x, _ = np.shape(result)

        if image_a:
            self.image_a_matrix = result
        else:
            self.image_b_matrix = result

        # return of we are not allowed to resize, or we don't need to.
        if not perform_resize or not rescale:
            return

        # resize the image
        self.resize_image(image_a)

    @staticmethod
    def short_circuit(args: CompareImageArguments, sc_size: bool, sc_hash: bool):
        """
        Perform short circuit execution on the side of the slave. Allows for faster processing on the side of the
        database.

        The behaviour, if the arguments for short-circuiting are not provided is that the program will continue as
        usual but emit a warning so the programmer is aware that an error occurred.

        :param args: the CompareImageArguments to be short-circuited.
        :param sc_size: if the size should be used as an indicator on which to short circuit
        :param sc_hash: if the hash should be used as an indicator on which to short circuit
        :return:
        """
        # faster if is outside.
        if sc_size:
            if args.img_a_size_x is None or args.img_a_size_y is None \
                    or args.img_b_size_x is None or args.img_b_size_y is None:

                print("WARNING: Size based short-circuiting initiated without providing a hash")
                return None

            # matching aspects search for positive result and negate the answer.
            if not ((args.img_a_size_x == args.img_b_size_x and args.img_a_size_y == args.img_b_size_y)
                    or (args.img_a_size_x == args.img_b_size_y and args.img_a_size_y == args.img_b_size_x)):
                # Need to create an instance...
                return CompareImageResults(key_a=args.key_a,
                                           key_b=args.key_b,
                                           error="",
                                           success=True,
                                           min_avg_diff=-1
                                           )  # genuine -1 difference

        # checking the hashes.
        if sc_hash:
            img_a_hash = [args.img_a_hash_0, args.img_a_hash_90, args.img_a_hash_180, args.img_a_hash_270]
            img_b_hash = [args.img_b_hash_0, args.img_b_hash_90, args.img_b_hash_180, args.img_b_hash_270]

            # make sure the fields are populated
            for hb in img_b_hash:
                if hb is None:
                    print("WARNING: Hash based short-circuiting initiated without providing a hash")
                    return None

            # make sure the fields are populated and perform the all to all comparison at the same time.
            for ha in img_a_hash:
                if ha is None:
                    print("WARNING: Hash based short-circuiting initiated without providing a hash")
                    return None

                for hb in img_b_hash:
                    # Hashes match, we proceed with the comparison
                    if ha == hb:
                        return None

            return CompareImageResults(key_a=args.key_a,
                                       key_b=args.key_b,
                                       error="",
                                       success=True,
                                       min_avg_diff=-1
                                       )  # genuine -1 difference

        # Nothing selected, don't return anything.
        return None

    def __image_loader(self, img_path: str, source: str) -> Tuple[Union[np.ndarray, None], str, bool]:
        """
        Private function that handles the basic loading and type conversion for an image. Errors are returned as a
        result and not stored in the class because if you load thumbnails, the error has not to be as severe as to
        prevent the computation from completing. That's why it's returned and the caller needs to determine what
        happens with the error.

        :param img_path: path to load from.
        :param source: the source of the image. Used for the error message
        :return: image or none, error message, if image needs to be rescaled
        """
        # load from fs
        try:
            img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        except Exception as e:
            err_str = f"Error {source} failed to load with:\n {e}"
            return None, err_str, False

        # assert type
        if type(img) != np.ndarray:
            err_str = f"Error {source} failed to load because the image is not of type np.ndarray"
            return None, err_str, False

        # convert grayscale to rgb
        if len(img.shape) == 2:
            img = skimage.color.gray2rgb(img)

        # assert length of image
        img = img[..., 0:3]

        # if one aspect is not matching, rescale the image
        scale = img.shape[0] != self.target_size_x or img.shape[1] != self.target_size_y
        return img, "", scale

    def store_image(self, img_a: bool = True):
        """
        Stores the image to file given by the thumbnail path. This will OVERWRITE a preexisting image.

        :param img_a: if image_matrix_a or image_matrix_b is to be stored to its respective thumbnail path.
        :return:
        """
        name = "<EMPTY>"
        try:
            if img_a:
                name = "image a"
                cv2.imwrite(self.thumb_a_path, self.image_a_matrix)
            else:
                name = "image b"
                cv2.imwrite(self.thumb_b_path, self.image_b_matrix)
        except Exception as e:
            self.error = f"Failed to save {name} to File with error: \n{e}"

    def resize_image(self, image_a: bool = True):
        """
        Resize image to image_size provided in the CompareImageArguments object.

        :param image_a: if the image_a should be resized or image_b
        :return:
        """
        img_str = "image_a" if image_a else "image_b"
        try:
            if image_a:
                self.image_a_matrix = cv2.resize(self.image_a_matrix, dsize=(self.target_size_x, self.target_size_y),
                                                 interpolation=cv2.INTER_CUBIC)
            else:
                self.image_b_matrix = cv2.resize(self.image_b_matrix, dsize=(self.target_size_x, self.target_size_y),
                                                 interpolation=cv2.INTER_CUBIC)
        except Exception as e:
            self.error = f"Error resizing {img_str} failed with:\n {e}"

    def img_rot(self, img_a: bool = True):
        """
        Rotate image by 90 degrees.

        :param img_a: if the image_a should be rotated or image_b
        :return:
        """
        img_str = "image_a" if img_a else "image_b"
        try:
            if img_a:
                self.image_a_matrix = np.rot90(self.image_a_matrix, k=1, axes=(0, 1))
            else:
                self.image_b_matrix = np.rot90(self.image_b_matrix, k=1, axes=(0, 1))
        except Exception as e:
            self.error = f"Error rotating {img_str} failed with:\n {e}"

    def compare_images(self):
        """
        Compare the images and store the result in the class.

        :return:
        """
        # check if the images are loaded
        if self.image_a_matrix is None:
            self.error = "Error image_a is not loaded."
            return
        if self.image_b_matrix is None:
            self.error = "Error image_b is not loaded."
            return

        # compare 0 degrees
        self.diff_0 = self.compare_func(self.image_a_matrix, self.image_b_matrix)

        # compare 90 degrees
        self.img_rot(True)
        self.diff_90 = self.compare_func(self.image_a_matrix, self.image_b_matrix)

        # compare 180 degrees
        self.img_rot(True)
        self.diff_180 = self.compare_func(self.image_a_matrix, self.image_b_matrix)

        # compare 270 degrees
        self.img_rot(True)
        self.diff_270 = self.compare_func(self.image_a_matrix, self.image_b_matrix)

        # rotate back for reuse.
        self.img_rot(True)

    def create_compare_result(self):
        """
        Create a CompareImageResult object from the class.

        :return:
        """
        min_diff = min(self.diff_0, self.diff_90, self.diff_180, self.diff_270)
        return CompareImageResults(key_a=self.processing_args.key_a,
                                   key_b=self.processing_args.key_b,
                                   error=self.error,
                                   success=self.error == "",
                                   min_avg_diff=min_diff if self.error == "" else -1,
                                   )

    def store_plt_on_threshold(self):
        """
        Shorthand to store the plot if the threshold is reached and the storing of the plot is desired.

        :return:
        """
        min_diff = min(self.diff_0, self.diff_90, self.diff_180, self.diff_270)
        if self.processing_args.store_compare and self.processing_args.compare_threshold > min_diff:
            self.create_compare_plot()

    def create_compare_plot(self):
        """
        Create a plot of the two images that are deemed to be similar and store it in predefined path.

        :return:
        """
        fig = plt.figure()
        min_diff = min(self.diff_0, self.diff_90, self.diff_180, self.diff_270)
        plt.suptitle(f"MSE: {min_diff:.2f}")

        # plot first image
        ax = fig.add_subplot(1, 2, 1)
        ax.title.set_text(os.path.basename(self.processing_args.img_a))
        plt.imshow(self.image_a_matrix, cmap=plt.cm.gray)
        plt.axis("off")

        # plot second image
        ax = fig.add_subplot(1, 2, 2)
        ax.title.set_text(os.path.basename(self.processing_args.img_b))
        plt.imshow(self.image_b_matrix, cmap=plt.cm.gray)
        plt.axis("off")

        # Don't show plot, clears the figure and an empty plot is aved.
        # plt.show(block=False)
        # show the images
        plt.savefig(self.processing_args.store_path)
        plt.close()

    def compute_img_hashes(self, img_a: bool = True):
        """
        Compute hash_prefix for duplicate detection.

        :param img_a: If image a should be hashed or image b
        :return:
        """
        # load from attributes
        if img_a:
            image_mat = np.copy(self.image_a_matrix)
            default_path = self.thumb_a_path
            name = "image a"
        else:
            image_mat = np.copy(self.image_b_matrix)
            default_path = self.thumb_b_path
            name = "image b"

        # should be sanitized by the main process.
        assert 8 > self.preprocessing_args.amount > -8, "amount exceeding range"

        # compute_new_paths
        p, e = os.path.splitext(default_path)
        path_0 = f"{p}_0{e}"
        path_90 = f"{p}_90{e}"
        path_180 = f"{p}_180{e}"
        path_270 = f"{p}_270{e}"

        try:
            # shift only if the amount is non-zero
            if self.preprocessing_args.amount > 0:
                image_mat = np.right_shift(image_mat, self.preprocessing_args.amount)
            elif self.preprocessing_args.amount < 0:
                image_mat = np.left_shift(image_mat, abs(self.preprocessing_args.amount))

            # store rot0 with shift
            cv2.imwrite(path_0, image_mat)

            # rot 90
            image_mat = np.rot90(image_mat, k=1, axes=(0, 1))
            cv2.imwrite(path_90, image_mat)

            # rot 180
            image_mat = np.rot90(image_mat, k=1, axes=(0, 1))
            cv2.imwrite(path_180, image_mat)

            # rot 270
            image_mat = np.rot90(image_mat, k=1, axes=(0, 1))
            cv2.imwrite(path_270, image_mat)

            # need to compute file hash since writing the
            hash_0 = hash_file(path_0)
            hash_90 = hash_file(path_90)
            hash_180 = hash_file(path_180)
            hash_270 = hash_file(path_270)

            # shouldn't be allowed to fail
            os.remove(path_0)
            os.remove(path_90)
            os.remove(path_180)
            os.remove(path_270)

        except Exception as e:
            self.error = f"Error hashing {name}:\n {e}"
            return

        self.hash_0 = hash_0
        self.hash_90 = hash_90
        self.hash_180 = hash_180
        self.hash_270 = hash_270
