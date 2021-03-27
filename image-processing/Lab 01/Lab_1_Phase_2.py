import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

img = mpimg.imread('cameraman.tif')

plt.figure(1)
plt.imshow(img,cmap = "gray")

fig2=plt.figure(2)

subplot2=fig2.add_subplot(2, 3, 2)
plt.imshow(img,cmap = "gray")
subplot2.set_title('Original_Image')

subplot2=fig2.add_subplot(2, 3, 4)
plt.imshow(img,cmap = "gray",vmin=3, vmax=103)
subplot2.set_title('3 to 103')

subplot2=fig2.add_subplot(2, 3, 5)
plt.imshow(img,cmap = "gray",vmin=103, vmax=203)
subplot2.set_title('103 to 203')

subplot2=fig2.add_subplot(2, 3, 6)
plt.imshow(img,cmap = "gray",vmin=203, vmax=255)
subplot2.set_title('203 to 255')

plt.show()


