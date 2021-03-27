import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from skimage import data
import math



def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

#-------------------------main program---------------------------------

img = mpimg.imread('football.jpg',format=str)


grayscale_image=rgb2gray(img)

grayscale_image=np.around(grayscale_image)
grayscale_image=np.uint8(grayscale_image)


plt.figure(1)
plt.imshow(img)
plt.suptitle('RGB')

plt.figure(2)
plt.imshow(grayscale_image,cmap="gray")
plt.suptitle('Grayscale')

plt.show()
