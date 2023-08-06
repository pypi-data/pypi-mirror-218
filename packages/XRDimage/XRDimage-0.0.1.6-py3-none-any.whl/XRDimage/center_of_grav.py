from PIL import Image

def find_center_of_gravity(image):
    """
    Centering method by weighing every pixel using its intensity.
    Returns the coordinates of the "center of gravity" of the image.

    Authors:
        Ethan Fang
    
    :param image: Input PIL image file for centering.
    :type image: PIL.Image.Image
    :return: The weighted X and Y coordinates of the center of gravity.
    :rtype: Tuple[float, float]
    """

    grayscale_image = image.convert("L")
    width, height = grayscale_image.size
    sumX, sumY, total = 0, 0, 0

    for x in range(width):
        for y in range(height):
            intensity = grayscale_image.getpixel((x, y))
            sumX += intensity * x
            sumY += intensity * y
            total += intensity

    weightedX = sumX / total
    weightedY = sumY / total
    return weightedX, weightedY

    '''
    CHANGELOG:

    v0_1 (July 10 2023) 
    '''

