import matplotlib.pyplot as plt
import numpy as np

def fspecial_gauss2D(shape,sigma):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h


#
#symmetrical_filter=fspecial_gauss2D((50,50),3.5)
#
#grid = np.random.random((10,10))
#fig, (ax1) = plt.subplots(nrows=1, figsize=(6,10))
#
#ax1.imshow(symmetrical_filter, extent=[0,100,0,100], aspect='auto')
#ax1.set_title('Auto-scaled Aspect')
#
#plt.tight_layout()
#plt.show()
#
