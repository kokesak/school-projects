import matplotlib.pyplot as plt
import matplotlib.image as mpimg



img = mpimg.imread('cameraman.tif',format=str)

plt.figure(1)
plt.imshow(img,cmap = "gray")

plt.savefig('my_cameraman.png')

mpimg.imsave('my_cameraman2.png',img,cmap = "gray")
