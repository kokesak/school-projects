#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.color import rgb2gray

import image_formats_and_conversions as tools


# In[2]:


img = mpimg.imread('moonlanding.png')
grayscale_image = rgb2gray(img)


# ## Two dimensional Fourier Transform

# In[3]:


grayscale_image_DFT = np.fft.fft2(grayscale_image)

grayscale_image_DFT_normalized = tools.normalize_fft_image(grayscale_image_DFT)
grayscale_image_DFT_normalized = tools.float_to_uint8(grayscale_image_DFT_normalized)

plt.imshow(grayscale_image_DFT_normalized, cmap="gray")


# ## Two dimensional inverse Fourier Transform

# In[4]:


grayscale_image_inverted_DFT = np.fft.ifft2(grayscale_image)

grayscale_image_inverted_DFT_normalized = tools.normalize_fft_image(grayscale_image_inverted_DFT)
grayscale_image_inverted_DFT_normalized = tools.float_to_uint8(grayscale_image_inverted_DFT_normalized)

plt.imshow(100*grayscale_image_inverted_DFT_normalized, cmap="gray")


# ## Two dimensional centered Fourier Transform

# In[5]:


grayscale_image_centered_DFT = np.fft.fftshift(grayscale_image_DFT)

grayscale_image_centered_DFT_normalized = tools.normalize_fft_image(grayscale_image_centered_DFT)
grayscale_image_centered_DFT_normalized = tools.float_to_uint8(grayscale_image_centered_DFT_normalized)

plt.imshow(grayscale_image_centered_DFT_normalized,cmap="gray")


# In[ ]:





# ## Ideal Low Pass Filter
# To filter in the frequency field we must follow the following steps:
# 1. Create a sphere in the center of the image with a specific radius to hold specific frequencies.
# 2. Do DFT and then DC-DFT on our image.
# 3. We multiply the sphere with our DC-DFT image
# 4. Calculate the inverse I-DFT
# 5. Transform the image into an image with absolute values ​​from 0 to 1
#
# ### 1. Create a sphere in the center of the image with a specific radius to hold specific frequencies.

# In[6]:


columns, rows = grayscale_image.shape[:2]

katheta = np.linspace(-127, 128, rows)
orizontia = np.linspace(-127, 128, columns)
katheta


# In[7]:


x,y = np.meshgrid(katheta, orizontia)
x,y


# In[8]:


apostasi = np.sqrt(np.power(x,2)+np.power(y,2))
apostasi


# In[9]:


katofli = apostasi < 15
plt.imshow(apostasi, cmap='gray')


# ### 2. Κάνουμε DFT και μετά DC-DFT στην εικόνα μας.

# In[10]:


grayscale_image_DFT = np.fft.fft2(grayscale_image)

grayscale_image_centered_DFT = np.fft.fftshift(grayscale_image_DFT)
grayscale_image_centered_DFT_normalized = tools.normalize_fft_image(grayscale_image_centered_DFT)

grayscale_image_centered_DFT_normalized = tools.float_to_uint8(grayscale_image_centered_DFT_normalized)

plt.imshow(grayscale_image_centered_DFT_normalized, cmap='gray')


# 3. Πολλαπλασιάζουμε την σφαίρα με την DC-DFT εικόνα μας

# In[11]:


mask_circle = katofli * grayscale_image_centered_DFT
mask_circle_normalized = tools.normalize_fft_image(mask_circle)
mask_circle_final = tools.float_to_uint8(mask_circle_normalized)

plt.imshow(mask_circle_final, cmap='gray')


# ### 4. Υπολογίζουμε τον αντίστροφο I-DFT

# In[12]:


filtered_image = np.fft.ifft2(mask_circle)
grayscale_image_inverted_DFT_normalized = tools.normalize_fft_image(filtered_image)

plt.imshow(grayscale_image_inverted_DFT_normalized, cmap='gray')


# ### 5. Μετασχηματίζουμε την εικόνα σε εικόνα με απόλυτες τιμές απο 0 έως 1

# In[13]:


filtered_image_normalized = np.abs(filtered_image)
filtered_image_normalized = tools.float_to_float64(filtered_image_normalized)
plt.imshow(filtered_image_normalized, cmap='gray')


# In[14]:


figure1=plt.figure(figsize=(15,10))

subplot1=figure1.add_subplot(2,2,1)
plt.imshow(grayscale_image, cmap="gray")
subplot1.set_title('Grayscale_Image')

subplot1=figure1.add_subplot(2,2,2)
plt.imshow(grayscale_image_centered_DFT_normalized, cmap="gray")
subplot1.set_title('Grayscale_Image_Centered_DFT')

subplot1=figure1.add_subplot(2,2,3)
plt.imshow(mask_circle_normalized, cmap="gray")
subplot1.set_title('mask_circle')

subplot1=figure1.add_subplot(2,2,4)
plt.imshow(filtered_image_normalized, cmap="gray")
subplot1.set_title('Filtered_image')


# ## Butterworth-low-pass filters
# - Ideal low-pass filters are not hardware feasible. In addition, they create ringing effect images due to the abrupt change of Hideal from value 1 to value 0.
# - Butterworth low-pass filters (BLPF) have a transfer function H of 1 form (n is the order of the filter):
#! [image.png] (attachment: image.png)

# In[15]:


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


# ![image.png](attachment:image.png)

# In[16]:


Grayscale_Image_DFT=np.fft.fft2(grayscale_image)
Grayscale_Image_Centered_DFT=np.fft.fftshift(Grayscale_Image_DFT)

Grayscale_Image_Centered_DFT_normalized=np.log(1+np.abs(Grayscale_Image_Centered_DFT))
Grayscale_Image_Centered_DFT_Final=tools.float_to_uint8(Grayscale_Image_Centered_DFT_normalized)

#-----------------------------------------------------------------------------------------------------------

mask_circle_n_1=katofli_n_1*Grayscale_Image_Centered_DFT
mask_circle_normalized_n_1=np.log(1+np.abs(mask_circle_n_1))
mask_circle_final_n_1=tools.float_to_uint8(mask_circle_normalized_n_1)

#------------------------------------------------------------------------------------------------------------
Filtered_image_n_1=np.fft.ifft2(mask_circle_n_1)
Filtered_image_normalized_n_1=np.abs(Filtered_image_n_1)
Filtered_image_final_n_1=tools.float_to_float64(Filtered_image_normalized_n_1)
#------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------

mask_circle_n_2=katofli_n_2*Grayscale_Image_Centered_DFT
mask_circle_normalized_n_2=np.log(1+np.abs(mask_circle_n_2))
mask_circle_final_n_2=tools.float_to_uint8(mask_circle_normalized_n_2)

#------------------------------------------------------------------------------------------------------------
Filtered_image_n_2=np.fft.ifft2(mask_circle_n_2)
Filtered_image_normalized_n_2=np.abs(Filtered_image_n_2)
Filtered_image_final_n_2=tools.float_to_float64(Filtered_image_normalized_n_2)
#------------------------------------------------------------------------------------------------------------


figure1=plt.figure(1, figsize=(14, 14))

subplot1=figure1.add_subplot(3,3,1)
plt.imshow(grayscale_image,cmap="gray")
subplot1.set_title('Grayscale_Image')

subplot1=figure1.add_subplot(3,3,2)
plt.imshow(Grayscale_Image_Centered_DFT_Final,cmap="gray")
subplot1.set_title('Grayscale_Image_Centered_DFT')

subplot1=figure1.add_subplot(3,3,3)
plt.imshow(mask_circle_final_n_1,cmap="gray")
subplot1.set_title('mask_circle_n_1')

subplot1=figure1.add_subplot(3,3,4)
plt.imshow(Filtered_image_final_n_1,cmap="gray")
subplot1.set_title('Filtered_image_n_1')

subplot1=figure1.add_subplot(3,3,5)
plt.imshow(mask_circle_final_n_2,cmap="gray")
subplot1.set_title('mask_circle_n_2')

subplot1=figure1.add_subplot(3,3,6)
plt.imshow(Filtered_image_final_n_2,cmap="gray")
subplot1.set_title('Filtered_image_n_2')

figure1.tight_layout()

plt.show()

# ## Excercise
# Read the image moonlanding.png. Create a butterworth filter by calculating the first 4 orders of the filter based on 15. Display these images in a subplot along with the original image to see the comparison. Then change the base to the value that you think is the best result and repeat the previous procedure. Finally in a figure show each result from the 4 classes with base 15 and the 4 classes with the base you used. Save your code along with the figures you created and upload it as DIP_LAB08_AM.zip where your registration number is AM.

# In[ ]:





# In[ ]:




