import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from skimage.filters import threshold_otsu
from skimage import measure
import scipy
import skimage as image_tool

grayscale_image = mpimg.imread('coins.png')
grayscale_image = (grayscale_image * 255).round().astype(np.uint8)

plt.figure(1)
plt.imshow(grayscale_image,cmap="gray")
plt.title('Original image-Coins')


thresh = threshold_otsu(grayscale_image)
Binary_image = grayscale_image > thresh
Binary_image=Binary_image.astype(int)

plt.figure(2)
plt.imshow(Binary_image,cmap=plt.cm.gray)
plt.title('Binary image with holes')

Binary_image=scipy.ndimage.morphology.binary_fill_holes(Binary_image)#Fill image's holes
Binary_image=Binary_image.astype(int)

plt.figure(3)
plt.imshow(Binary_image,cmap=plt.cm.gray)
plt.title('Binary image WITHOUT holes')

[Labeled_image,num_of_neighbors] = measure.label(Binary_image,  connectivity=1,background=False,return_num=True) #Get labeeled image on 4 neighbors

plt.figure(4)
plt.imshow(Labeled_image==9,cmap=plt.cm.gray)
plt.title('8th coin of binary image')


Overall_connected_list=image_tool.measure.regionprops(Labeled_image) #Find the conected pixels


plt.figure(5)   
plt.imshow(Labeled_image,cmap=plt.cm.gray)

for i in range(num_of_neighbors):
    plt.annotate(i, xy=(Overall_connected_list[i].centroid[1],Overall_connected_list[i].centroid[0]),color='red')
plt.show()
