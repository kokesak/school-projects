import matplotlib.pyplot as plt
import numpy as np
import skimage as image_tool
from skimage import measure








Image_Binary=[[0, 0, 0, 0, 0, 0, 0, 0],[0, 1, 1, 0, 0, 1, 1, 1],
              [0, 1, 1, 0, 0, 0, 1, 1],[0, 1, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0, 0, 0],[0, 0, 0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 1, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0]]

Image_Binary=np.asarray(Image_Binary, dtype=np.bool)
Image_Binary=Image_Binary.astype(int)

plt.figure(1)
plt.imshow(Image_Binary,cmap=plt.cm.gray)
plt.title('Binary_Image')





Overall_connected_list=image_tool.measure.regionprops(Image_Binary) #Find the conected pixels

Coords_of_connected_components=Overall_connected_list[0].coords #Save coords in a variable

[Labeled_image,num_of_neighbors] = measure.label(Image_Binary,background=False,return_num=True, connectivity=2) #Get labeeled image on 8 neighbors

Group_connected_list=image_tool.measure.regionprops(Labeled_image) #Find the conected pixels

plt.figure(2)
plt.imshow(Labeled_image,cmap="gray")
plt.title('Labelled_Pseudo_grayscale Image')




[Labeled_image,num_of_neighbors] = measure.label(Image_Binary,background=False,return_num=True, connectivity=2) #Get labeeled image on 8 neighbors

Group_connected_list=image_tool.measure.regionprops(Labeled_image)

plt.figure(3)
plt.imshow(Labeled_image,cmap="gray")
plt.title('Labelled_Pseudo_grayscale Image_2')



plt.show()





