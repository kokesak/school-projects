import matplotlib.pyplot as plt
import numpy as np



Image_Binary=[[0, 0, 0, 0, 0, 0, 0, 0],[0, 1, 1, 0, 0, 1, 1, 1],
              [0, 1, 1, 0, 0, 0, 1, 1],[0, 1, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0, 0, 0],[0, 0, 0, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 1, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0]]

Image_Binary=np.asarray(Image_Binary, dtype=np.bool)
Image_Binary=Image_Binary.astype(int)

plt.figure(1)
plt.imshow(Image_Binary,cmap=plt.cm.gray)
plt.title('Binary_Image')
plt.show()
