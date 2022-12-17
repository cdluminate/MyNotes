'''
http://scikit-image.org/
http://scikit-image.org/docs/dev/user_guide.html
http://scikit-image.org/docs/dev/user_guide/transforming_image_data.html
'''
import sys, os, re
from skimage import data, io, filters
from PIL import Image
import numpy as np

#image = data.coins()
image = Image.open(sys.argv[1]).convert('L')
#image = Image.open(sys.argv[1]).convert('1')
image = np.array(image)
print(image.shape)
io.imshow(image)
io.show()

edges = filters.sobel(image)
io.imshow(edges)
io.show()

image = Image.fromarray(image.astype(np.uint8))
