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

def find_contours_8(img):
    coords_x = []
    coords_y = []

    for i in range(len(img)-1):
        for j in range(len(img)-1):
            if (img[i,j]==1 and (img[i,j-1]==0 or img[i,j+1]==0 or img[i-1,j]==0 or img[i+1,j]==0
                                or img[i-1,j-1]==0 or img[i+1,j-1]==0 or img[i-1,j+1]==0 or img[i+1,j+1]==0)):
                coords_x.append(i)
                coords_y.append(j)

    coords_x = np.asarray(coords_x, dtype=np.int32)
    coords_y = np.asarray(coords_y, dtype=np.int32)

    coords = np.transpose(np.vstack((coords_x,coords_y)))  

    return coords



# ## Find contours

# In[4]:


contours = find_contours_4(image_binary)

new_binary = np.zeros((10,10))

new_binary = np.asarray(new_binary, dtype=np.bool)
new_binary = new_binary.astype(int)

new_binary[contours[:,0], contours[:,1]] = 1

plt.figure(2)
plt.imshow(new_binary, cmap='gray')
plt.title('Binary_perimeter_Image')
plt.show()

# ## Find contours of another image

# In[5]:


image_binary=np.zeros((100,100))

image_binary[30:50,30:50]=1
image_binary[51:70,51:70]=1

image_binary=np.asarray(image_binary, dtype = np.bool)
image_binary=image_binary.astype(int)

plt.figure(1)
plt.imshow(image_binary,cmap=plt.cm.gray)


# In[6]:


coords = find_contours_8(image_binary)

new_binary = np.zeros((100,100))

new_binary = np.asarray(new_binary, dtype=np.bool)
new_binary = new_binary.astype(int)

new_binary[coords[:,0], coords[:,1]] = 1

plt.figure(2)
plt.imshow(new_binary,cmap=plt.cm.gray)
plt.title('Binary_perimeter_Image')
plt.show()

# ## Exercise
# Implement the chain algorithm for 8 neighbors and plot figures for both of the images.

# In[ ]:




