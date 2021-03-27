import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import numpy as np
from skimage import data, color
from skimage.filters import threshold_otsu
import math

from skimage.transform import resize, rotate

from skimage.util import random_noise
from skimage.color import rgb2gray

from scipy.ndimage import convolve

from skimage import measure


def my_rgb2grayscale(image):
    r = image[:,:,0]
    g = image[:,:,1]
    b = image[:,:,2]

    return 0.2989 * r + 0.5870 * g + 0.1140 * b


def gscale2binary(grayscale_image):
    thresh = threshold_otsu(grayscale_image)
    binary_image = grayscale_image > thresh
    return binary_image.astype(int)

def fspecial_gauss2D(shape,sigma):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h


def my_gaussian_noise(img,std):
    mean = 0.0   # some constant
    noisy_img = img + np.random.normal(mean, std, img.shape)
    noisy_img_clipped = np.clip(noisy_img, 0, 255)
    noisy_img_clipped = np.around(noisy_img_clipped)
    noisy_img_clipped = np.asarray(noisy_img_clipped, dtype=np.uint8)

    return noisy_img_clipped




#
# copied from https://github.com/MeteHanC/Python-Median-Filter/blob/master/MedianFilter.py
#
def median_filter(data, filter_size):
    temp = []
    indexer = filter_size // 2
    data_final = []
    data_final = np.zeros((len(data),len(data[0])))
    for i in range(len(data)):

        for j in range(len(data[0])):

            for z in range(filter_size):
                if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                    for c in range(filter_size):
                        temp.append(0)
                else:
                    if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                        temp.append(0)
                    else:
                        for k in range(filter_size):
                            temp.append(data[i + z - indexer][j + k - indexer])

            temp.sort()
            data_final[i][j] = temp[len(temp) // 2]
            temp = []
    return data_final



def my_median_filter(data, filter_size):
    temp = []
    indexer = filter_size // 2
    window = [
        (i, j)
        for i in range(-indexer, filter_size-indexer)
        for j in range(-indexer, filter_size-indexer)
    ]
    index = len(window) // 2
    for i in range(len(data)):
        for j in range(len(data[0])):
            data[i][j] = sorted(
                0 if (
                    min(i+a, j+b) < 0
                    or len(data) <= i+a
                    or len(data[0]) <= j+b
                ) else data[i+a][j+b]
                for a, b in window
            )[index]
    return data


#-------------------------main program---------------------------------

img = mpimg.imread('aloe-plant-pot.jpg')

r=img[:,:,0]
 
g=img[:,:,1]
 
b=img[:,:,2]


# ----- Task 1
fig1 = plt.figure(1, figsize=(8.5, 8.5))

subplot1=fig1.add_subplot(2,3,1)
plt.imshow(r,cmap="gray")
subplot1.set_title('Red channel Image')

subplot1=fig1.add_subplot(2,3,2)
plt.imshow(g,cmap="gray")
subplot1.set_title('Green channel Image')

subplot1=fig1.add_subplot(2,3,3)
plt.imshow(b,cmap="gray")
subplot1.set_title('Blue channel Image')

grayscale_image = my_rgb2grayscale(img)
subplot1=fig1.add_subplot(2,3,4)
plt.imshow(grayscale_image,cmap="gray")
subplot1.set_title("Grayscale Image")

binary_image = gscale2binary(grayscale_image)
subplot1=fig1.add_subplot(2,3,5)
plt.imshow(binary_image,cmap="gray")
subplot1.set_title("Binary Image")

fig1.tight_layout()



# ----- Task 2
fig2 = plt.figure(2, figsize=(5.5, 5.5))

subplot2=fig2.add_subplot(1,1,1)
histogram_values=np.histogram(grayscale_image,bins=256)
hist1=plt.hist(grayscale_image, facecolor='blue', alpha=1)
plt.title("Histogram of Grayscale Image")

fig2.tight_layout()




# ----- Task 3
fig3 = plt.figure(3, figsize=(7.5,7.5))

# Transpose image
subplot3=fig3.add_subplot(1,3,1)
transposed_image = np.transpose(grayscale_image)
plt.imshow(transposed_image,cmap="gray")
subplot3.set_title("Transposed Image")

# Resize
subplot3=fig3.add_subplot(1,3,2)
resized_image = resize(grayscale_image, (300, 255), anti_aliasing=True)
plt.imshow(resized_image, cmap='gray')
subplot3.set_title("Resized Image 300x255")

# Rotate
subplot3=fig3.add_subplot(1,3,3)
rotated_image = rotate(resized_image, 45, resize=True)
plt.imshow(rotated_image, cmap="gray")
subplot3.set_title("Rotated Image 45 L")

fig3.tight_layout()



# ----- Task 4

fig4 = plt.figure(4, figsize=(8.5,8.5))

grayscale_image = rgb2gray(img)
subplot4=fig4.add_subplot(3,3,1)
plt.imshow(grayscale_image,cmap="gray")
subplot4.set_title("Grayscale Image")

#gaussian_noise_image=random_noise(grayscale_image, mode='gaussian')
#subplot4=fig4.add_subplot(3,3,2)
#plt.imshow(gaussian_noise_image,cmap="gray")
#subplot4.set_title("Gaussian Noise Image")

gaussian_noise_image2=my_gaussian_noise(grayscale_image, 0.5) # 0.5 is here for std
subplot4=fig4.add_subplot(3,3,3)
plt.imshow(gaussian_noise_image2,cmap="gray")
subplot4.set_title("My Gaussian Noise 0,5 std")


# ----- Task 5
image_filtered_by_mask = median_filter(gaussian_noise_image2,5)
subplot4=fig4.add_subplot(3,3,4)
plt.imshow(image_filtered_by_mask,cmap="gray")
subplot4.set_title("filtered by median filter")

image_filtered_by_mask = my_median_filter(gaussian_noise_image2,5)
subplot4=fig4.add_subplot(3,3,5)
plt.imshow(image_filtered_by_mask,cmap="gray")
subplot4.set_title("filtered by my median filter")


# ----- Task 6
gaussian_mask=fspecial_gauss2D((5,5),0.5)

# Application of the mask (5x5 filter with sigma = 0.5)
image_filtered_by_mask=convolve(gaussian_noise_image2,gaussian_mask)

# Normalize image values
image_filtered_by_mask=(image_filtered_by_mask - np.min(image_filtered_by_mask))*255/(np.max(image_filtered_by_mask)-np.min(image_filtered_by_mask))

image_filtered_by_mask=np.around(image_filtered_by_mask)
image_filtered_by_mask=np.asarray(image_filtered_by_mask, dtype=np.uint8)

subplot4=fig4.add_subplot(3,3,6)
plt.imshow(image_filtered_by_mask,cmap="gray")
subplot4.set_title("mask 5x5 (convolve)")




fig4.tight_layout()

# ----- Task 7

img2 = mpimg.imread('noise_world_map.png')
grayscale_image = my_rgb2grayscale(img2)
columns=len(grayscale_image)
rows=len(grayscale_image[0])

katheta = np.linspace(-127, 128,rows )
orizontia = np.linspace(-127, 128, columns)

x,y = np.meshgrid(katheta, orizontia)

apostasi=np.sqrt(np.power(x,2)+np.power(y,2))
n=1
base=15
katofli_n_1=1/(1+(np.power(apostasi,2*n)/np.power(base,2*n)))
n=2
base=25
katofli_n_2=1/(1+(np.power(apostasi,2*n)/np.power(base,2*n)))


grayscale_image_DFT=np.fft.fft2(grayscale_image)
grayscale_image_centered_DFT=np.fft.fftshift(grayscale_image_DFT)

grayscale_image_centered_DFT_normalized=np.log(1+np.abs(grayscale_image_centered_DFT))

mask_circle=katofli_n_1*grayscale_image_centered_DFT
mask_circle_normalized=np.log(1+np.abs(mask_circle))

filtered_image = np.fft.ifft2(mask_circle)
filtered_image_normalized = np.abs(filtered_image)


fig5 = plt.figure(5, figsize=(8.5,8.5))

#subplot5=fig5.add_subplot(2,2,3)
#plt.imshow(grayscale_image_centered_DFT_normalized,cmap="gray")
#subplot5.set_title("Grayscale_Image_Centered_DFT")

#subplot5=fig5.add_subplot(2,2,4)
#plt.imshow(mask_circle_normalized,cmap="gray")
#subplot5.set_title("Mask_Circle")

subplot5=fig5.add_subplot(2,2,1)
plt.imshow(filtered_image_normalized,cmap="gray")
subplot5.set_title("Filtered Image")

subplot5=fig5.add_subplot(2,2,2)
plt.imshow(img2,cmap="gray")
subplot5.set_title("Original Image")


fig5.tight_layout()
# ----- Task show South America
fig6 = plt.figure(6,figsize=(10.5,10.5))

subplot6=fig6.add_subplot(1,2,1)
binary_map = gscale2binary(filtered_image_normalized)
plt.imshow(binary_map,cmap="gray")
subplot6.set_title("Binary map")


[labeled_image,num_of_neighbors] = measure.label(binary_map,  connectivity=2,background=False,return_num=True) #Get labeeled image on 8 neighbors

subplot6=fig6.add_subplot(1,2,2)
plt.imshow(labeled_image==15,cmap="gray")
subplot6.set_title("South America")


fig6.tight_layout()
plt.show()
