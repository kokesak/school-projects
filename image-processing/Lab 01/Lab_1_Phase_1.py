import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('cameraman.tif')

fig = plt.figure(1)
imgplot=plt.imshow(img)

fig2 = plt.figure(2)
imgplot=plt.imshow(img, cmap = "gray")   
plt.show()
