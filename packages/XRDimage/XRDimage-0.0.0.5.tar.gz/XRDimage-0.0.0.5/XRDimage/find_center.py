import numpy as np
from PIL import Image as im
from PIL import ImageOps, ImageChops

def create_circular_mask(h, w, outer_radius, inner_radius, center=None):
    """
    Create a circular ring mask for specified radii.

    Authors:
        Weiqi Yue, Gabriel Ponon, Zhuldyz Ualikhankyzy, Nathaniel K. Tomczak

    :param h: Height of the mask.
    :type h: int
    :param w: Width of the mask.
    :type w: int
    :param outer_radius: Outer radius for the mask.
    :type outer_radius: float
    :param inner_radius: Inner radius for the mask.
    :type inner_radius: float
    :param center: Coordinate tuple of the center of the mask. Uses the middle of the image if None.
    :type center: tuple, optional
    :return: The circular mask.
    :rtype: numpy.ndarray
    """
    if center is None:
        center = (int(w/2), int(h/2))
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y - center[1])**2)
    mask = (dist_from_center <= outer_radius) & (dist_from_center >= inner_radius)
    return mask

def define_mask(h=2048, w=2048, inner_radius=40, white_width=8, black_width=10):
    """
    Returns a multi-ring mask that can be used to filter an XRD image.

    Authors:
        Weiqi Yue, Gabriel Ponon, Zhuldyz Ualikhankyzy, Nathaniel K. Tomczak

    :param h: Height of the mask.
    :type h: int
    :param w: Width of the mask.
    :type w: int
    :param inner_radius: Inner radius of the first ring.
    :type inner_radius: int, optional
    :param white_width: Width of the transparent ring portions.
    :type white_width: int, optional
    :param black_width: Width of the opaque ring portions.
    :type black_width: int, optional
    :return: The multi-ring mask.
    :rtype: numpy.ndarray
    """
    center = (int(w/2), int(h/2))
    result_mask = np.zeros((h, w))
    for i in range(0, 50):
        start = inner_radius + (white_width + black_width) * i
        end = start + white_width
        raw_mask = create_circular_mask(w, h, outer_radius=end, inner_radius=start)
        one_array = np.ones((w, h))
        mask = raw_mask * one_array
        result_mask = np.add(result_mask, mask)
    return result_mask

def add_margin(pil_img, top, right, bottom, left, color):
    """
    Add margins around the border of an image.

    Authors:
        Weiqi Yue, Gabriel Ponon, Zhuldyz Ualikhankyzy, Nathaniel K. Tomczak

    :param pil_img: Input PIL image to which margins are added.
    :type pil_img: PIL.Image
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
    :return: The image with added margins.
    :rtype: PIL.Image
    """
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = im.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def find_center(img, mask=None):
    """
    Apply a mask to the central region of interest on an XRD image and find the coordinates of maximum intensity.

    Authors:
        Weiqi Yue, Gabriel Ponon, Zhuldyz Ualikhankyzy, Nathaniel K. Tomczak

    :param img: Input PIL XRD image to find the ring center.
    :type img: PIL.Image
    :param mask: The mask to use. If None, a mask will be generated through the define_mask function.
    :type mask: numpy.ndarray, optional
    :return: The coordinates of the maximum intensity.
    :rtype: tuple
    """
    if mask is None:
        mask = define_mask()

    mask = im.fromarray(mask)

    img_padding = add_margin(img, 300, 300, 300, 300, 0)
    mask_padding = add_margin(mask, 300, 300, 300, 300, 0)

    max_i = -99999
    cord = np.nan
    p = 0

    for i in range(-20, 20):
        for j in range(-20, 20):
            offset_img = np.roll(mask_padding, i, axis=0)
            offset_img = np.roll(offset_img, j, axis=1)
            aa = img_padding * offset_img
            c = aa.sum()
            if c > max_i:
                max_i = c
                cord = [i, j]
            elif c == max_i:
                p += 1

    final_x = cord[1] + 1024
    final_y = cord[0] + 1024

    return final_x, final_y

    '''
    CHANGELOG:

    v0_1 (Jul 23 2022) 
    '''
