# ## Excercise
# 1. Read the image rice.png
# 2. Using which mask (structuring element and function) can we improve the quality of the displayed objects? Justify your answer
# 3. Display in a figure with a sublot (with the corresponding dimensions) the original image as well as the images after applying the mask
# 4. Save the .ipynb file with your password, as well as the figure with the two images
# 5. Upload the compressed folder with your files to eclass named div_lab5_AM.zip, where your registration number is AM


# In[ ]:

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy
import scipy.ndimage
from skimage.filters import threshold_otsu
from skimage.morphology import binary_dilation, binary_erosion
import skimage.morphology


def gaussian_noise(img,std):
    mean = 0.0   # some constant
    noisy_img = img + np.random.normal(mean, std, img.shape)
    noisy_img_clipped = np.clip(noisy_img, 0, 255)
    noisy_img_clipped = np.around(noisy_img_clipped)
    noisy_img_clipped = np.asarray(noisy_img_clipped, dtype=np.uint8)

    return noisy_img_clipped


image = mpimg.imread('rice.png')
gaussian_image = gaussian_noise(image, 0.0001)


filter_3_by_3 = np.ones((3,3))/9  # 3x3 table of aces (1), multiplied by 1/9
filter_5_by_5 = np.ones((5,5))/25

image_filtered_by_3 = scipy.ndimage.convolve(gaussian_image, filter_3_by_3) # Multidimensional convolution
#The array is convolved with the given kernel
#here we use as kernels the filters we created
image_filtered_by_5 = scipy.ndimage.convolve(gaussian_image, filter_5_by_5)




figure1 = plt.figure(1, figsize=(10.5, 10.5))

subplot1 = figure1.add_subplot(2,2,1)
plt.imshow(image, cmap='gray')
subplot1.set_title('Original_Image')

subplot1 = figure1.add_subplot(2,2,2)
plt.imshow(image_filtered_by_3, cmap='gray')
subplot1.set_title('image_filtered_by_3')

subplot1 = figure1.add_subplot(2,2,3)
plt.imshow(image_filtered_by_5, cmap='gray')
subplot1.set_title('image_filtered_by_5')

subplot1 = figure1.add_subplot(2,2,4)
plt.imshow(gaussian_image, cmap='gray')
subplot1.set_title('gaussian_noise')

figure1.tight_layout()
plt.show()



