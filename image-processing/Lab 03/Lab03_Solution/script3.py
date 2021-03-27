import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from skimage.filters import threshold_otsu
from skimage import measure
import scipy
import skimage as image_tool

grayscale_image = mpimg.imread('rice.png')
grayscale_image = (grayscale_image * 255).round().astype(np.uint8)

thresh = threshold_otsu(grayscale_image)
Binary_image = grayscale_image > thresh
Binary_image=Binary_image.astype(int)

Binary_image=scipy.ndimage.morphology.binary_fill_holes(Binary_image)#Fill image's holes
Binary_image=Binary_image.astype(int)

# Get labeeled image on 4 neighbors
[labeled_rice_4,num_of_neighbors] = measure.label(Binary_image,  neighbors=4,background=False,return_num=True)

#Get labeeled image on 8 neighbors
[labeled_rice_8,num_of_neighbors] = measure.label(Binary_image,  neighbors=8,background=False,return_num=True)

#plt.figure(4)
#plt.imshow(Labeled_image==0,cmap=plt.cm.gray)
#plt.title('8th coin of binary image')

Overall_connected_list = image_tool.measure.regionprops(labeled_rice_4) #Find the conected pixels

figure = plt.figure()

plt.subplot(2, 2, 1)
plt.imshow(labeled_rice_4, cmap = 'gray')
plt.title('4 neigbours')

plt.subplot(2, 2, 2)
plt.imshow(labeled_rice_8, cmap = 'gray')
plt.title('8 neighbours')

plt.subplot(2, 2, 3)
plt.imshow(labeled_rice_4 == 100, cmap = 'gray')
plt.title('4 neigbours - 100th grain')

plt.subplot(2, 2, 4)
plt.imshow(labeled_rice_8 == 100, cmap = 'gray')
plt.title('8 neighbours - 100th grain')

figure.tight_layout()
plt.savefig('my_rice.png')
plt.show()

#plt.figure(5)   
#plt.imshow(Labeled_image,cmap=plt.cm.gray)

#for i in range(num_of_neighbors):
#    plt.annotate(i, xy=(Overall_connected_list[i].centroid[1],Overall_connected_list[i].centroid[0]),color='red')
#plt.show()
