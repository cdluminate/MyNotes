'''
skimage segmentation
http://scikit-image.org/docs/dev/user_guide/tutorial_segmentation.html
http://scikit-image.org/docs/dev/auto_examples/segmentation/plot_join_segmentations.html#sphx-glr-auto-examples-segmentation-plot-join-segmentations-py
'''
import sys, os, re
import numpy as np
from skimage import filters, measure, segmentation, color, data
import pylab as lab
from PIL import Image
import IPython

img = data.coins()
if len(sys.argv) > 1:
    img = Image.open(sys.argv[1]).convert('RGB')
    img = np.array(img)

seg = segmentation.slic(img, n_segments=300, sigma=1, compactness=30)
lab.imshow(seg)
lab.show()

color = color.label2rgb(seg, image=img, image_alpha=0.5)

lab.imshow(color)
lab.show()

np.set_printoptions(threshold=np.inf)
IPython.embed()
