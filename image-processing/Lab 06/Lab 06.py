#!/usr/bin/env python
# coding: utf-8

# In[24]:


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import f_special_script as f_special
import skimage
import scipy
import scipy.ndimage
import Image_formats_and_conversions as tools


# In[8]:


Original_image=mpimg.imread('cameraman.tif')


# ## Gaussian filters
# Gaussian filters can:
# 1. Produce noise in an image
# 2. Blur an image

# ### Add Gaussian noise to the image

# In[9]:


Image_Gaussian_noise=skimage.util.random_noise(Original_image, mode='gaussian')
Image_Gaussian_noise.shape


# ### Image Blur - Denoise-Smooth
# Create different gaussian masks

# In[10]:


#                                        hsize,sigma
Gauss_mask_1_5=f_special.fspecial_gauss2D((5,5),0.5)
Gauss_mask_2_5=f_special.fspecial_gauss2D((5,5),2.5)
Gauss_mask_3_5=f_special.fspecial_gauss2D((5,5),5.5)
                                                        # Gaussian peripheral symmetric filters (lowpassfilter)
                                                         # hsize size and sigma standard deviation (positive)
                                                        # Hsize can be a defining vector
                                                    # the number of rows / columns of h, or it can be a graded value
                                                             # so then h is a square array.
                                                               # Default values: hsize = [3,3], sigma = 0.5
Gauss_mask_1_7=f_special.fspecial_gauss2D((7,7),0.5)
Gauss_mask_2_7=f_special.fspecial_gauss2D((7,7),2.5)
Gauss_mask_3_7=f_special.fspecial_gauss2D((7,7),5.5)


# In[11]:


# Application of the first mask (5x5 filter with sigma = 0.5)
Image_filtered_by_mask_1_5=scipy.ndimage.convolve(Image_Gaussian_noise,Gauss_mask_1_5)

# Normalize image values
Image_filtered_by_mask_1_5=(Image_filtered_by_mask_1_5-np.min(Image_filtered_by_mask_1_5))*255/(np.max(Image_filtered_by_mask_1_5)-np.min(Image_filtered_by_mask_1_5))

Image_filtered_by_mask_1_5=np.around(Image_filtered_by_mask_1_5)
Image_filtered_by_mask_1_5=np.asarray(Image_filtered_by_mask_1_5, dtype=np.uint8)


# In[12]:


# Application of the second mask (5x5 filter with sigma = 2.5)
Image_filtered_by_mask_2_5=scipy.ndimage.convolve(Image_Gaussian_noise,Gauss_mask_2_5)

# Normalize image values
Image_filtered_by_mask_2_5=(Image_filtered_by_mask_2_5-np.min(Image_filtered_by_mask_2_5))*255/(np.max(Image_filtered_by_mask_2_5)-np.min(Image_filtered_by_mask_2_5))

Image_filtered_by_mask_2_5=np.around(Image_filtered_by_mask_2_5)
Image_filtered_by_mask_2_5=np.asarray(Image_filtered_by_mask_2_5, dtype=np.uint8)


# In[13]:


# Application of the third mask (5x5 filter with sigma = 5.5)
Image_filtered_by_mask_3_5=scipy.ndimage.convolve(Image_Gaussian_noise,Gauss_mask_3_5)

# Normalize image values
Image_filtered_by_mask_3_5=(Image_filtered_by_mask_3_5-np.min(Image_filtered_by_mask_3_5))*255/(np.max(Image_filtered_by_mask_3_5)-np.min(Image_filtered_by_mask_3_5))

Image_filtered_by_mask_3_5=np.around(Image_filtered_by_mask_3_5)
Image_filtered_by_mask_3_5=np.asarray(Image_filtered_by_mask_3_5, dtype=np.uint8)


# In[14]:


# Application of the fourth mask (7x7 filter with sigma = 0.5)
Image_filtered_by_mask_1_7=scipy.ndimage.convolve(Image_Gaussian_noise,Gauss_mask_1_7)

# Normalize image values
Image_filtered_by_mask_1_7=(Image_filtered_by_mask_1_7-np.min(Image_filtered_by_mask_1_7))*255/(np.max(Image_filtered_by_mask_1_7)-np.min(Image_filtered_by_mask_1_7))

Image_filtered_by_mask_1_7=np.around(Image_filtered_by_mask_1_7)
Image_filtered_by_mask_1_7=np.asarray(Image_filtered_by_mask_1_7, dtype=np.uint8)


# In[15]:


#Application of the fifth mask (7x7 filter with sigma = 2.5)
Image_filtered_by_mask_2_7=scipy.ndimage.convolve(Image_Gaussian_noise,Gauss_mask_2_7)

# Normalize image values
Image_filtered_by_mask_2_7=(Image_filtered_by_mask_2_7-np.min(Image_filtered_by_mask_2_7))*255/(np.max(Image_filtered_by_mask_2_7)-np.min(Image_filtered_by_mask_2_7))

Image_filtered_by_mask_2_7=np.around(Image_filtered_by_mask_2_7)
Image_filtered_by_mask_2_7=np.asarray(Image_filtered_by_mask_2_7, dtype=np.uint8)


# In[19]:


# Εφαρμογή της έκτης μάσκας (7x7 φίλτρο με sigma=5.5)
Image_filtered_by_mask_3_7=scipy.ndimage.convolve(Image_Gaussian_noise,Gauss_mask_3_7)

# Κανονικοποίηση τιμών εικόνας
Image_filtered_by_mask_3_7=(Image_filtered_by_mask_3_7-np.min(Image_filtered_by_mask_3_7))*255/(np.max(Image_filtered_by_mask_3_7)-np.min(Image_filtered_by_mask_3_7))

Image_filtered_by_mask_3_7=np.around(Image_filtered_by_mask_3_7)
Image_filtered_by_mask_3_7=np.asarray(Image_filtered_by_mask_3_7, dtype=np.uint8)


# ## Εμφανίσεις εικόνων

# In[18]:


figure1=plt.figure(1, figsize=(8.5, 8.5))

subplot1=figure1.add_subplot(1,2,1)
plt.imshow(Original_image,cmap='gray')
subplot1.set_title('Original_image')

subplot1=figure1.add_subplot(1,2,2)
plt.imshow(Image_Gaussian_noise,cmap='gray')
subplot1.set_title('Image_With_Gaussian_noise')

figure1.tight_layout()


# In[23]:


figure2=plt.figure(2, figsize=(10.5, 10.5))

subplot2=figure2.add_subplot(2,3,1)
plt.imshow(Image_filtered_by_mask_1_5,cmap='gray')
subplot2.set_title('5x5-sigma:0.5')

subplot2=figure2.add_subplot(2,3,2)
plt.imshow(Image_filtered_by_mask_2_5,cmap='gray')
subplot2.set_title('5x5-sigma:2.5')

subplot2=figure2.add_subplot(2,3,3)
plt.imshow(Image_filtered_by_mask_3_5,cmap='gray')
subplot2.set_title('5x5-sigma:5.5')

subplot2=figure2.add_subplot(2,3,4)
plt.imshow(Image_filtered_by_mask_1_7,cmap='gray')
subplot2.set_title('7x7-sigma:0.5')

subplot2=figure2.add_subplot(2,3,5)
plt.imshow(Image_filtered_by_mask_2_7,cmap='gray')
subplot2.set_title('7x7-sigma:2.5')

subplot2=figure2.add_subplot(2,3,6)
plt.imshow(Image_filtered_by_mask_3_7,cmap='gray')
subplot2.set_title('7x7-sigma:5.5')

figure2.tight_layout()


# ## Εκθετικός Μετασχηματικός - Exponential Transform

# In[25]:


Original_image2=mpimg.imread('cameraman.tif')
Office_image=mpimg.imread('office.jpg')


# In[26]:


Grayscale_image_office=tools.rgb_to_gray(Office_image)   #another way to convert to grayscale


# In[27]:


#Take the log of it. Add 1 to avoid taking log of zero
log_zero_avoidance=1

b=255/(np.log(1+255*log_zero_avoidance))

Image_exponetial_transform =(1/log_zero_avoidance)* (np.exp(Original_image/b)-1)

Image_office_exponetial_transform =(1/log_zero_avoidance)* (np.exp(Grayscale_image_office/b)-1)


# In[28]:


figure3=plt.figure(3, figsize=(7.5, 7.5))

subplot3=figure3.add_subplot(2,2,1)
plt.imshow(Original_image,cmap='gray')
subplot3.set_title('Original_image')

subplot3=figure3.add_subplot(2,2,2)
plt.imshow(Image_exponetial_transform,cmap='gray')
subplot3.set_title('Image_with_exponetial_transform')

subplot3=figure3.add_subplot(2,2,3)
plt.imshow(Grayscale_image_office,cmap='gray')
subplot3.set_title('Original_grayscale_image')

subplot3=figure3.add_subplot(2,2,4)
plt.imshow(Image_office_exponetial_transform,cmap='gray')
subplot3.set_title('Image_with_exponetial_transform')

figure3.tight_layout()


# ## Λογαριθμικός Μετασχηματισμός - Logarithmic Transform

# In[29]:


Image_logarithmic_transform=b*np.log(1+log_zero_avoidance*Original_image)
Image_logarithmic_transform=tools.float_to_uint8(Image_logarithmic_transform)


Image_office_logarithmic_transform=b*np.log(1+log_zero_avoidance*Grayscale_image_office)
Image_office_logarithmic_transform=tools.float_to_uint8(Image_office_logarithmic_transform)


# In[31]:


figure4=plt.figure(4, figsize=(7.5, 7.5))

subplot4=figure4.add_subplot(2,2,1)
plt.imshow(Original_image,cmap='gray')
subplot4.set_title('Original_image')

subplot4=figure4.add_subplot(2,2,2)
plt.imshow(Image_logarithmic_transform,cmap='gray')
subplot4.set_title('Image_with_logarithmic_transform')

subplot4=figure4.add_subplot(2,2,3)
plt.imshow(Grayscale_image_office,cmap='gray')
subplot4.set_title('Original_grayscale_image')

subplot4=figure4.add_subplot(2,2,4)
plt.imshow(Image_office_logarithmic_transform,cmap='gray')
subplot4.set_title('Image_with_logarithmic_transform')

figure4.tight_layout()


# ## Ιστόγραμμα Εικόνας
# The histogram in the context of image processing is the operation by which the occurrences of each intensity value in the image is shown

# In[37]:


figure5=plt.figure(5, figsize=(7.5, 7.5))

subplot5=figure5.add_subplot(2,2,1)
plt.imshow(Grayscale_image_office,cmap='gray')
subplot5.set_title('Original_grayscale_image')

subplot5=figure5.add_subplot(2,2,2)
plt.imshow(Image_office_exponetial_transform,cmap='gray')
subplot5.set_title('Image_with_exponetial_transform')

subplot5=figure5.add_subplot(2,2,3)
histogram_values=np.histogram(Grayscale_image_office,bins=256)
hist1= plt.hist(Grayscale_image_office, facecolor='blue', alpha=1)
plt.title("Histogram of Original Image")
plt.show()

subplot5=figure5.add_subplot(2,2,4)
histogram_values=np.histogram(Image_exponetial_transform,bins=256)
hist1= plt.hist(Image_office_exponetial_transform, facecolor='blue', alpha=0.5)
plt.title("Histogram of Transformed Image")
plt.show()

figure5.tight_layout()


# ## Excercise
# 1. Read the image football.jpg
# 2. Turn it into a grayscale
# 3. Calculate the exponential transformation of the image
# 4. Apply gaussian noise to the image
# 5. Remove the noise (denoise-smooth) from the image using a guassian filter with hsize = 9 and sigma = 6.5
# 6. Find the histograms of all the images (grayscale, exponential, gaussian noise, smoothed)
# 7. Display all images in a subplot
# 8. BONUS: Display all histograms in a single plot, with different colors

# In[ ]:




