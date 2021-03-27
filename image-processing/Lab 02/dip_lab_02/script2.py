import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from skimage import data
from skimage.color import rgb2gray
from skimage.transform import rescale, resize, downscale_local_mean

image = rgb2gray(data.astronaut())
plt.imshow(image, cmap = "gray")

# Transpose image
image_transposed = np.transpose(image)
plt.imshow(image_transposed, cmap = "gray")

# Rescale
image_rescaled = rescale(image, 0.2, anti_aliasing=False)
plt.imshow(image_rescaled, cmap='gray')

# Smoother image
image_rescaled = rescale(image, 0.2, anti_aliasing=True)
plt.imshow(image_rescaled, cmap='gray')

# Resize image
image_resized = resize(image, (image.shape[0] // 4, image.shape[1] // 4), anti_aliasing=True)
plt.imshow(image_resized, cmap='gray')

# Downscale image
image_downscaled = downscale_local_mean(image, (4, 3))
plt.imshow(image_downscaled, cmap='gray')

####
fig, axes = plt.subplots(nrows=2, ncols=2)
ax = axes.ravel()

#ax[0].imshow(image_transposed, cmap='gray')
ax[0].imshow(image, cmap='gray')
ax[0].set_title("Original image")

ax[1].imshow(image_rescaled, cmap='gray')
ax[1].set_title("Rescaled image (aliasing)")

ax[2].imshow(image_resized, cmap='gray')
ax[2].set_title("Resized image (no aliasing)")

ax[3].imshow(image_downscaled, cmap='gray')
ax[3].set_title("Downscaled image (no aliasing)")

ax[0].set_xlim(0, 512)
ax[0].set_ylim(512, 0)
plt.tight_layout()
plt.show()
