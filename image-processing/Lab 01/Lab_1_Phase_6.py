import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#-------------------------main program---------------------------------

img = mpimg.imread('football.jpg')

r=img[:,:,0]
 
g=img[:,:,1]
 
b=img[:,:,2]
 
fig1=plt.figure(1)

subplot1=fig1.add_subplot(2,2,1)
plt.imshow(img,cmap="gray")
subplot1.set_title('Original Image')

subplot1=fig1.add_subplot(2,2,2)
plt.imshow(r,cmap="gray")
subplot1.set_title('Red channel Image')

subplot1=fig1.add_subplot(2,2,3)
plt.imshow(g,cmap="gray")
subplot1.set_title('Green channel Image')

subplot1=fig1.add_subplot(2,2,4)
plt.imshow(b,cmap="gray")
subplot1.set_title('Blue channel Image')

plt.show()
