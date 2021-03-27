import numpy as np
from skimage.filters import threshold_otsu

def float_to_uint8(Image):
    
    Image=(Image-np.min(Image))*255/(np.max(Image)-np.min(Image))
    Image=np.around(Image)
    Image=np.asarray(Image, dtype=np.uint8)
    
    return Image


def rgb_to_gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def gray_to_binary(Grayscale_image):
    thresh = threshold_otsu(Grayscale_image)
    Binary_image = Grayscale_image > thresh
    Binary_image=np.asarray(Binary_image, dtype=np.int32) 
    
    return Binary_image

def float_to_float64(Image):
    
    Image=(Image-np.min(Image))*255/(np.max(Image)-np.min(Image))
    Image=np.around(Image)

    
    return Image
