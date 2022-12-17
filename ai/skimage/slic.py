# http://scikit-image.org/docs/stable/auto_examples/segmentation/plot_segmentations.html#sphx-glr-auto-examples-segmentation-plot-segmentations-py

from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import matplotlib.pyplot as plt
import argparse

# construct the argument parser and parse the arguments
ag = argparse.ArgumentParser()
ag.add_argument("-i", "--image", required = True, help = "Path to the image")
ag.add_argument('-c', '--compact', type = int, default=10)
ag = ag.parse_args()

# load the image and convert it to a floating point data type
image = img_as_float(io.imread(ag.image))

# loop over the number of segments
for numSegments in (300,): #(100, 200, 300):
	# apply SLIC and extract (approximately) the supplied number
	# of segments
	segments = slic(image, n_segments = numSegments, sigma = 5,
                compactness = ag.compact)
 
	# show the output of SLIC
	fig = plt.figure("Superpixels -- %d segments" % (numSegments))
	ax = fig.add_subplot(1, 1, 1)
	ax.imshow(mark_boundaries(image, segments))
	plt.axis("off")
 
# show the plots
plt.show()
