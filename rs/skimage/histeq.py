'''
http://scikit-image.org/docs/stable/auto_examples/color_exposure/plot_equalize.html#sphx-glr-auto-examples-color-exposure-plot-equalize-py
'''
import sys, os, re
import argparse
import numpy as np
from skimage import data, img_as_float, exposure, io
import pylab as lab
from PIL import Image

img = data.moon()
if len(sys.argv) > 1:
    img = Image.open(sys.argv[1]).convert('RGB')
    img = np.array(img)

def show(img, text='', bins=256):
    img = img_as_float(img)
    lab.imshow(img)
    lab.title(f'image {text}')
    lab.show()

    cdf, bins = exposure.cumulative_distribution(img, bins)
    lab.hist(img.ravel(), bins=bins, histtype='step')
    lab.title(f'histogram {text}')
    lab.show()

    lab.plot(bins, cdf)
    lab.title(f'CDF {text}')
    lab.show()

show(img, 'original')

# Contrast stretching
img_rescale = exposure.rescale_intensity(img, in_range=(
    np.percentile(img, 2), np.percentile(img, 98)
    ))
show(img_rescale, 'rescale')

# histogram equilization
img_eq = exposure.equalize_hist(img)
show(img_eq, 'hist eq')

# adaptive equalization
img_adaeq = exposure.equalize_adapthist(img, clip_limit=0.03)
show(img_adaeq, 'adapt hist eq')
