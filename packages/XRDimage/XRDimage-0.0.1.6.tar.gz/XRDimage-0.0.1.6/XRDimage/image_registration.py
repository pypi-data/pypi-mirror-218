from PIL import Image as im
import numpy as np

def register_image(img, input_center_x, input_center_y):
  '''
    Outputs a PIL image shifted so that the specified 'true' center
    coordinates can be found in the geometric center of the image frame.
    The image is cropped to remove trailing regions and resized to the 
    original image size.

    Authors:
        Weiqi Yue, Gabriel Ponon, Zhuldyz Ualikhankyzy, Nathaniel K. Tomczak

    :param img: The input PIL image to center and register.
    :type img: PIL.Image
    :param input_center_x: The 'true' center x-coordinate identified for the image.
    :type input_center_x: float
    :param input_center_y: The 'true' center y-coordinate identified for the image.
    :type input_center_y: float
'''

  
  ## Define the center of the image and the offset between it and the center of the ring
  dim_x = img.size[0]
  dim_y = img.size[1]
  true_center_x = dim_x/2
  true_center_y = dim_y/2
  offset_x = int(round(true_center_x - input_center_x))
  offset_y = int(round(true_center_y - input_center_y))

  ### move rings to the center of the image and use dark pixel 
  offset_img = np.roll(img, offset_y, axis=0)
  offset_img = np.roll(offset_img, offset_x, axis=1)
  offset_image = im.fromarray(offset_img)

  # capture non-cropped section of the image and save to new variable
  if offset_y >= 0 and offset_x <= 0:
  # assign new array to contents of desired image
    new_img = offset_img[offset_y:dim_y, 0: dim_x + offset_x]
  elif offset_y < 0 and offset_x <= 0:
    new_img = offset_img[0:dim_y + offset_y, 0: dim_x + offset_x]
  elif offset_y >= 0 and offset_x > 0:
    new_img = offset_img[offset_y: dim_y, offset_x:dim_x]
  else:
    new_img = offset_img[0:dim_y + offset_y, offset_x: dim_x]

  # convert pixel value array into image
  new_img = im.fromarray(new_img)

  # resize the image
  new_img = new_img.resize((dim_x, dim_y))
  return new_img

  '''
  CHANGELOG:

  v0_1 (Jul 23 2022) 
  '''