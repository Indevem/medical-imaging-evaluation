%matplotlib inline
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

fig, axs = plt.subplots(5, 4, figsize=(50,50))



pathlist = Path("Origin").rglob('*.png')
imgnames = []
for path in pathlist:
    imgnames.append(str(path)[7:-4])

#for img in imgnames:
#  print(img)
i = 0
axs[0,0].set_title("Experts")
axs[0,1].set_title("Algorithm1")
axs[0,2].set_title("Algorithm2")
axs[0,3].set_title("Algorithm3")
for img in imgnames:
    orig_temp = mpimg.imread('Origin/'+img+'.png')
    axs[i,0].imshow(orig_temp, cmap='gray', interpolation='nearest')
    axs[i,0].imshow(mpimg.imread('Expert/'+img+'_expert.png'), cmap='gray', alpha=0.5)
    axs[i,1].imshow(orig_temp, cmap='gray')
    axs[i,1].imshow(mpimg.imread('sample_1/'+img+'_s1.png'), cmap='gray', alpha=0.5)
    axs[i,2].imshow(orig_temp, cmap='gray')
    axs[i,2].imshow(mpimg.imread('sample_2/'+img+'_s2.png'), cmap='gray', alpha=0.5)
    axs[i,3].imshow(orig_temp, cmap='gray')
    axs[i,3].imshow(mpimg.imread('sample_3/'+img+'_s3.png'), cmap='gray', alpha=0.5)
    i+=1
    if i==5:
        break


plt.show()
