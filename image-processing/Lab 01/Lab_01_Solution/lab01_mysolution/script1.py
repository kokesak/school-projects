import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from skimage import data, color
from skimage.filters import threshold_otsu
import math

#
# Convert RGB image to grayscale colors
#
def rgb2grayscale(image):
    r = image[:,:,0]
    g = image[:,:,1]
    b = image[:,:,2]

    return 0.2989 * r + 0.5870 * g + 0.1140 * b

#
# Convert grayscale image to binary image
#
def gscale2binary(grayscale_image):
    thresh = threshold_otsu(grayscale_image)
    binary_image = grayscale_image > thresh
    return binary_image.astype(int)

# --------- main ----------------- #
figure = plt.figure(figsize=(12,8))

# --------- Original RGB --------- #
image = mpimg.imread('football.jpg', format=str)

subplot = figure.add_subplot(2,2,1)
plt.imshow(image)
subplot.set_title('RGB Image')

# -------- Grayscale ------------- #
grayscale_image = rgb2grayscale(image)
# TODO Why it is here?
#grayscale_image=np.around(grayscale_image)
#grayscale_image=np.uint8(grayscale_image)

subplot = figure.add_subplot(2,2,3)
plt.imshow(grayscale_image, cmap="gray")
subplot.set_title('Gray Image')

# ------- HSV Image -------------- #
hsv_image = color.rgb2hsv(image)

subplot = figure.add_subplot(2,2,2)
plt.imshow(hsv_image)
subplot.set_title('HSV Image')

# ------- Binary Image ----------- #
binary_image = gscale2binary(grayscale_image)

subplot = figure.add_subplot(2,2,4)
plt.imshow(binary_image, cmap="gray")
subplot.set_title('Binary Image')


# show image
#plt.show()

# save image
plt.savefig('lab1.png')
