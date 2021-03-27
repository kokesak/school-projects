import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg

A=[[1, 2, 3, 4],[5, 6, 7, 8],[ 9, 10, 11, 12],[13, 14, 15, 16]]
A=np.asarray(A, dtype=np.int32)

plt.figure(1)

plt.imshow(A,cmap="gray")
plt.suptitle('Grayscale')

B=A+10
C=A-10

Image_A=np.hstack((A,B,C))
Image_B=np.hstack((C,B,A))
Image_C=np.hstack((B,A,C))

Image=np.vstack((Image_A,Image_B,Image_C))

np.min(A)
np.min(Image)
np.max(Image)

Image2=Image
Image2 = Image2.clip(min=0)
Image2=np.uint8(Image2)

plt.figure(2)

plt.imshow(Image,cmap="gray")
plt.suptitle('First-float32 image')

plt.figure(3)
plt.imshow(Image2,cmap="gray")
plt.suptitle('Second-uint8 image')

mpimg.imsave('Image2_uint8.png',Image2,cmap = "gray")

img2 = mpimg.imread('Image2_uint8.png')

plt.figure(4)
plt.imshow(img2,cmap = "gray")
plt.show()
