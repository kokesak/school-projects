import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from skimage import data
from skimage.color import rgb2gray
from skimage.transform import rescale, resize, downscale_local_mean, rotate


# 1. Create a 100x100 table A with random values.
A = np.random.rand(100,100)
#print(A)
#plt.imshow(A, cmap='gray')
#plt.show()

# 2. Save in table B the normalization of table A to grayscale values [0-255] and uint8 encoding
B = (A-np.min(A))*255/(np.max(A)-np.min(A))
B = np.asarray(B, dtype=np.uint8)
#print(B)
plt.imshow(B, cmap='gray')

# 3. Save table B as a jpg image
mpimg.imsave('B_Image.jpg', B, cmap='gray')

# 4. Read the jpg image you created and rotate it 135 degrees (variable C)
C = mpimg.imread('B_Image.jpg') 
C = rotate(C, 135)
plt.imshow(C, cmap='gray')

# 5. Create a 2x3 subplot and display the tables in order:
# - A first row second column
# - B second row first column
# - C second row third column
figure = plt.figure()

subplot = figure.add_subplot(2, 3, 2)
plt.imshow(A)
subplot.set_title('A')

subplot = figure.add_subplot(2, 3, 4)
plt.imshow(B, cmap='gray')
subplot.set_title('B')

subplot = figure.add_subplot(2, 3, 6)
plt.imshow(C, cmap='gray')
subplot.set_title('C')

figure.tight_layout()

# 7. Save all the files in a zip named dip_lab2_AM.zip where your registration number is AM.
#plt.show()
figure.savefig('figure.png')
