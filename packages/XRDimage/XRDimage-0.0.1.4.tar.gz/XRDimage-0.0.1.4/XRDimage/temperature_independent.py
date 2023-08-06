from PIL import Image as im
import numpy as np
from PIL import ImageOps, ImageChops


def add_margin(pil_img, top, right, bottom, left, color):
    '''
    Image padding script, to add 300 pixels around the border of an XRD image
    so the images become 2048 plus 600 square matrices.

    Authors:
        Weiqi Yue, Gabriel Ponon, Zhuldyz Ualikhankyzy, Nathaniel K. Tomczak

    :param pil_img: Input PIL image to which margins are added.
    :type pil_img: PIL.Image.Image
    :param top: Size of the top margin.
    :type top: int
    :param right: Size of the right margin.
    :type right: int
    :param bottom: Size of the bottom margin.
    :type bottom: int
    :param left: Size of the left margin.
    :type left: int
    :param color: Color to overlay for margins.
    :type color: int or tuple
    :return: Resulting image with added margins.
    :rtype: PIL.Image.Image
    '''
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = im.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def reshape(input_img):
    '''
    Change image array shape to fit resize operation.

    Authors:
        Weiqi Yue, Gabriel Ponon, Zhuldyz Ualikhankyzy, Nathaniel K. Tomczak

    :param input_img: The input PIL image to reshape.
    :type input_img: PIL.Image.Image
    :return: Reshaped image array.
    :rtype: numpy.ndarray
    '''
    result_img = input_img.resize((4194304,1))
    result_img = np.array(result_img)
    result_img = result_img[0]
    return result_img


def resize_image(img, ref_path, r_only=False, img_only=False, fixed_ratio=None):
    '''
    Resize image to desired 2048 x 2048 size by finding optimum ratio.
    The optimum is determined by minimizing a correlation coefficient between
    the input image and a reference image.

    Authors:
        Weiqi Yue, Gabriel Ponon, Zhuldyz Ualikhankyzy, Nathaniel K. Tomczak

    :param img: Input PIL image to resize.
    :type img: PIL.Image.Image
    :param ref_path: Full path to the reference image.
    :type ref_path: str
    :param r_only: True when the output is the ratio number only. (default: False)
    :type r_only: bool
    :param img_only: True when the output is the PIL image only. (default: False)
    :type img_only: bool
    :param fixed_ratio: The value to fix the ratio for computation. Set to None to retrieve the ratio value automatically. (default: None)
    :type fixed_ratio: float or None
    :return: Resized image or ratio value, depending on the parameters.
    :rtype: PIL.Image.Image or float
    '''
    # add padding to PIL image input
    im_padding = add_margin(img, 300, 300, 300, 300, 0)
    ref = im.open(ref_path)
    C2 = reshape(ref)

    old_size = im_padding.size
    desired_size = 2048

    # ratio of diameter
    if fixed_ratio is not None:
        ratio = np.asarray([fixed_ratio])  # fixed ratio
    else:
        ratio = np.arange(0.9, 1.1, 0.005)  # create a series of ratios, change parameters here

    max_cor = -99999
    max_img = np.nan

    # iterate over ratios to find configuration with the lowest correlation
    for i in ratio:
        new_size = tuple([int(x * i) for x in old_size])  # set reference size

        # resize padding image
        im_re = im_padding.resize(new_size)

        # create a new image and paste the resized one onto it
        new_im = im.new(im_padding.mode, (desired_size, desired_size))
        new_im.paste(im_re, ((desired_size - new_size[0]) // 2, (desired_size - new_size[1]) // 2))
        max_img = new_im  # set max to current since there is only one

        # skip correlation if fixed ratio is not defined
        if fixed_ratio is None:
            # calculate correlation
            C1 = reshape(new_im)
            cor = np.corrcoef(C1, C2)  # find correlation value between image and reference
            aa = cor[0, 1]
            if max_cor < aa:
                max_cor = aa
                max_img = new_im
                r = i  # set min correlation ratio value as output ratio
        else:
            r = i

    if r_only:
        return r
    elif img_only:
        return max_img
    else:
        return max_img, r


'''
CHANGELOG:

v0_1 (Jul 23 2022) - changed ratio range from 0.95 to 1.05 to 0.9 to 1.1
                   - fixed bad condition for fixed ratio
'''
