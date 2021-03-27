#!/usr/bin/env python
# coding: utf-8

# ## Imports

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import skimage
from skimage import measure


# ## Create a binary image

# In[2]:


image_binary=[[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 1, 1, 0],
              [0, 0, 0, 1, 1, 1, 1, 0],
              [0, 0, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 1, 1, 1, 0, 0],
              [0, 0, 1, 1, 1, 1, 0, 0],
              [0, 0, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]

image_binary = np.asarray(image_binary, dtype=np.bool)
image_binary = image_binary.astype(int)

plt.figure(1)
plt.imshow(image_binary, cmap='gray')
plt.title('Binary_Image')


# ## Implement the chain algorithm

# In[3]:


def find_contours_4(img):
    coords_x = []
    coords_y = []

    for i in range(len(img)-1):
        for j in range(len(img)-1):
            if (img[i,j]==1 and (img[i,j-1]==0 or img[i,j+1]==0 or img[i-1,j]==0 or img[i+1,j]==0)):
                coords_x.append(i)
                coords_y.append(j)

    coords_x = np.asarray(coords_x, dtype=np.int32)
    coords_y = np.asarray(coords_y, dtype=np.int32)

    coords = np.transpose(np.vstack((coords_x,coords_y)))  

    return coords


# In[4]:


def find_contours_8(img):
    coords_x = []
    coords_y = []

    for i in range(len(img)-1):
        for j in range(len(img)-1):
            if (img[i,j]==1 and (img[i,j-1]==0 or img[i,j+1]==0 or img[i-1,j]==0 or img[i+1,j]==0 or img[i-1,j-1]==0 or img[i-1,j+1]==0 or img[i+1,j-1]==0 or img[i+1,j+1]==0)):
                coords_x.append(i)
                coords_y.append(j)

    coords_x = np.asarray(coords_x, dtype=np.int32)
    coords_y = np.asarray(coords_y, dtype=np.int32)

    coords = np.transpose(np.vstack((coords_x,coords_y)))  

    return coords


# ## Find contours

# In[5]:


contours = find_contours_4(image_binary)

New_Binary=np.zeros((10,10))

New_Binary=np.asarray(New_Binary, dtype=np.bool)
New_Binary=New_Binary.astype(int)

New_Binary[contours[:,0], contours[:,1]] = 1

plt.figure(2)
plt.imshow(New_Binary, cmap='gray')
plt.title('Binary_perimeter_Image with 4 neighbors')


# In[6]:


contours = find_contours_8(image_binary)

New_Binary=np.zeros((10,10))

New_Binary=np.asarray(New_Binary, dtype=np.bool)
New_Binary=New_Binary.astype(int)

New_Binary[contours[:,0], contours[:,1]] = 1

plt.figure(3)
plt.imshow(New_Binary, cmap='gray')
plt.title('Binary_perimeter_Image with 8 neighbors')


# ## Find contours of another image

# In[7]:


image_binary=np.zeros((100,100))

image_binary[30:51,30:51] = 1
image_binary[49:70,49:70] = 1

image_binary = np.asarray(image_binary, dtype = np.bool)
image_binary = image_binary.astype(int)

plt.figure(4)
plt.imshow(image_binary,cmap=plt.cm.gray)
plt.title('Binary_Image')


# In[8]:


coords = find_contours_4(image_binary)

new_binary = np.zeros((100,100))

new_binary = np.asarray(new_binary, dtype=np.bool)
new_binary = new_binary.astype(int)

new_binary[coords[:,0], coords[:,1]] = 1

plt.figure(5)
plt.imshow(new_binary,cmap=plt.cm.gray)
plt.title('Binary_perimeter_Image with 4 neighbors')

# In[9]:


coords = find_contours_8(image_binary)

new_binary = np.zeros((100,100))

new_binary = np.asarray(new_binary, dtype=np.bool)
new_binary = new_binary.astype(int)

new_binary[coords[:,0], coords[:,1]] = 1

plt.figure(6)
plt.imshow(new_binary,cmap=plt.cm.gray)
plt.title('Binary_perimeter_Image with 8 neighbors')

plt.show()
# In[ ]:




