#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.color import rgb2gray
from skimage.color import rgba2rgb

import image_formats_and_conversions as tools


# In[2]:


img = mpimg.imread('cameraman.png')
#grayscale_image = rgb2gray(img)
grayscale_image = rgb2gray(rgba2rgb(img))

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

plt.imshow(grayscale_image_inverted_DFT_normalized, cmap="gray")


# ## Two dimensional centered Fourier Transform

# In[5]:


grayscale_image_centered_DFT = np.fft.fftshift(grayscale_image_DFT)

grayscale_image_centered_DFT_normalized = tools.normalize_fft_image(grayscale_image_centered_DFT)
grayscale_image_centered_DFT_normalized = tools.float_to_uint8(grayscale_image_centered_DFT_normalized)

plt.imshow(grayscale_image_centered_DFT_normalized,cmap="gray")


# In[ ]:





# ## Ιδεατό Χαμηλοπερατό Φίλτρο
# Για να φιλτράρουμε στο πεδίο συχνοτήτων πρέπει να ακολουθήσουμε τα εξής βήματα:
# 1. Να δημιουργήσουμε μια σφαίρα στο κέντρο της εικόνας με συγκεκριμένη ακτίνα για να κρατήσει συγκεκριμένες συχνότητες.
# 2. Κάνουμε DFT και μετά DC-DFT στην εικόνα μας.
# 3. Πολλαπλασιάζουμε την σφαίρα με την DC-DFT εικόνα μας
# 4. Υπολογίζουμε τον αντίστροφο I-DFT
# 5. Μετασχηματίζουμε την εικόνα σε εικόνα με απόλυτες τιμές απο 0 έως 1
# 
# ### 1. Να δημιουργήσουμε μια σφαίρα στο κέντρο της εικόνας με συγκεκριμένη ακτίνα για να κρατήσει συγκεκριμένες συχνότητες.

# In[6]:


columns, rows = grayscale_image.shape[:2]

katheta = np.linspace(-127, 128, rows)
orizontia = np.linspace(-127, 128, columns)
orizontia


# In[7]:


x,y = np.meshgrid(katheta, orizontia)
x,y


# In[8]:


apostasi = np.sqrt(np.power(x,2)+np.power(y,2))
apostasi


# In[21]:


katofli = apostasi < 15
plt.imshow(apostasi, cmap='gray')


# ### 2. Κάνουμε DFT και μετά DC-DFT στην εικόνα μας.

# In[22]:


grayscale_image_DFT = np.fft.fft2(grayscale_image)

grayscale_image_centered_DFT = np.fft.fftshift(grayscale_image_DFT)
grayscale_image_centered_DFT_normalized = tools.normalize_fft_image(grayscale_image_centered_DFT)

grayscale_image_centered_DFT_normalized = tools.float_to_uint8(grayscale_image_centered_DFT_normalized)

plt.imshow(grayscale_image_centered_DFT_normalized, cmap='gray')


# 3. Πολλαπλασιάζουμε την σφαίρα με την DC-DFT εικόνα μας

# In[23]:


mask_circle = katofli * grayscale_image_centered_DFT
mask_circle_normalized = tools.normalize_fft_image(mask_circle)
mask_circle_final = tools.float_to_uint8(mask_circle_normalized)

plt.imshow(mask_circle_final, cmap='gray')


# ### 4. Υπολογίζουμε τον αντίστροφο I-DFT

# In[24]:


filtered_image = np.fft.ifft2(mask_circle)
grayscale_image_inverted_DFT_normalized = tools.normalize_fft_image(filtered_image)

plt.imshow(grayscale_image_inverted_DFT_normalized, cmap='gray')


# ### 5. Μετασχηματίζουμε την εικόνα σε εικόνα με απόλυτες τιμές απο 0 έως 1

# In[25]:


filtered_image_normalized = np.abs(filtered_image)
filtered_image_normalized = tools.float_to_float64(filtered_image_normalized)
plt.imshow(filtered_image_normalized, cmap='gray')


# In[26]:


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

plt.show()
# In[ ]:





# ## Άσκηση
# Επαναλάβετε όλη την διαδικασία με την χρήση της εικόνας 'football.jpg' αλλάζοντας το εύρος συχνοτήτων της εικόνας, έτσι ώστε να δημιουργείται περισσότερος θόρυβος. 
# #### Μόνο σωστές ασκήσεις θα γίνονται δεκτές!! 

# In[ ]:




