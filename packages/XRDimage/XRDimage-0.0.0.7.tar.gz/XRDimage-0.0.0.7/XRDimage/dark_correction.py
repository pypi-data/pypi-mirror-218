import numpy as np
from PIL import Image as im


def dark_correction(img, dark_file_path, threshold=16384):
    '''
    Apply darkness correction to the specified input file and output
    a dark-corrected PIL image.

    Authors: 
        Weiqi Yue, Gabriel Ponon, Zhuldyz Ualikhankyzy, Nathaniel K. Tomczak

    :param img: Input file image for dark correction.
    :type img: PIL.Image.Image
    :param dark_file_path: Full path to reference image whose pixels are subtracted from those of the input images.
    :type dark_file_path: str
    :param threshold: The intensity value below which the pixels are set to 0. (default: 16384)
    :type threshold: int
    :return: Dark-corrected PIL image.
    :rtype: PIL.Image.Image
    '''
    img_arr = np.array(img)  # open image as array
    img_dark = np.array(im.open(dark_file_path))  # open reference image as array

    # dark correction: subtract original image
    darkCor = img_arr - img_dark

    # set all negative values as 0
    darkCor[darkCor > threshold] = 0  # set threshold at given number
    save_img = im.fromarray(darkCor)
    return save_img

    '''
    CHANGELOG:

    v0_1 (Jul 23 2022) 
    '''
