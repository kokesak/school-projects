#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import Image_formats_and_conversions as tools
import f_special_script as f_special
import skimage
import scipy


# In[2]:


Original_image=mpimg.imread('football.jpg')

Grayscale_image=tools.rgb_to_gray(Original_image)
Grayscale_image=tools.float_to_uint8(Grayscale_image)


# In[3]:


#Take the log of it. Add 1 to avoid taking log of zero
log_zero_avoidance=1
b=255/(np.log(1+255*log_zero_avoidance))
Image_exponetial_transform =(1/log_zero_avoidance)* (np.exp(Grayscale_image/b)-1)
Image_exponetial_transform=tools.float_to_float64(Image_exponetial_transform)


# In[4]:


Image_Gaussian_noise=skimage.util.random_noise(Grayscale_image, mode='gaussian')
Image_Gaussian_noise=tools.float_to_float64(Image_Gaussian_noise)

Gauss_mask_1_5=f_special.fspecial_gauss2D((9,9),6.5)
Image_filtered_by_mask_9=scipy.ndimage.convolve(Image_Gaussian_noise,Gauss_mask_1_5)
Image_filtered_by_mask_9=tools.float_to_uint8(Image_filtered_by_mask_9)


# In[10]:


figure1=plt.figure(1, figsize=(8.5, 8.5))


subplot1=figure1.add_subplot(2,2,1)
plt.imshow(Grayscale_image,cmap='gray')
plt.axis('off')
subplot1.set_title('Original_grayscale_image',color='red')


subplot1=figure1.add_subplot(2,2,2)
plt.imshow(Image_exponetial_transform,cmap='gray')
plt.axis('off')
subplot1.set_title('Image_exponetial_transform',color='red')


subplot1=figure1.add_subplot(2,2,3)
plt.imshow(Image_Gaussian_noise,cmap='gray')
plt.axis('off')
subplot1.set_title('Image_Gaussian_noise',color='red')


subplot1=figure1.add_subplot(2,2,4)
plt.imshow(Image_filtered_by_mask_9,cmap='gray')
plt.axis('off')
subplot1.set_title('Image_filtered_by_mask_9',color='red')

figure1.tight_layout()


# In[13]:


figure2=plt.figure(2, figsize=(9.5, 9.5))

subplot1=figure2.add_subplot(4,1,1)
histogram_values=np.histogram(Grayscale_image,bins=256)
hist1= plt.hist(Grayscale_image, facecolor='blue', alpha=0.5)
plt.title("Histogram of Original_Grayscale_image",color='red',loc='left')
plt.show()

subplot1=figure2.add_subplot(4,1,2)
histogram_values=np.histogram(Image_exponetial_transform,bins=256)
hist1= plt.hist(Image_exponetial_transform, facecolor='red', alpha=0.5)
plt.title("Histogram of Image_exponetial_transform",color='red',loc='left')
plt.show()

subplot1=figure2.add_subplot(4,1,3)
histogram_values=np.histogram(Image_Gaussian_noise,bins=256)
hist1= plt.hist(Image_Gaussian_noise, facecolor='green', alpha=0.5)
plt.title("Histogram of Image_Gaussian_noise",color='red',loc='left')
plt.show()


subplot1=figure2.add_subplot(4,1,4)
histogram_values=np.histogram(Image_filtered_by_mask_9,bins=256)
hist1= plt.hist(Image_filtered_by_mask_9, facecolor='orange', alpha=0.5)
plt.title("Histogram of Image_filtered_by_mask_9",color='red',loc='left')
plt.show()

figure2.tight_layout()


# ## BONUS

# In[15]:


plt.figure(2, figsize=(9.5, 9.5))
histogram_values1=np.histogram(Grayscale_image,bins=256)
hist1= plt.hist(Grayscale_image, facecolor='blue', alpha=0.5)

histogram_values2=np.histogram(Image_exponetial_transform,bins=256)
hist2= plt.hist(Image_exponetial_transform, facecolor='red', alpha=0.5)

histogram_values3=np.histogram(Image_Gaussian_noise,bins=256)
hist3= plt.hist(Image_Gaussian_noise, facecolor='green', alpha=0.5)

histogram_values4=np.histogram(Image_filtered_by_mask_9,bins=256)
hist4= plt.hist(Image_filtered_by_mask_9, facecolor='orange', alpha=0.5)

#frequencies=[histogram_values1[0],histogram_values2[0],histogram_values3[0],histogram_values4[0]]
#plt.ylim(0,np.max(frequencies))
plt.show()


# In[ ]:




