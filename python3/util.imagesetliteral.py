#!/usr/bin/python3
from PIL import Image
import numpy as np
import h5py
import argparse
import random
import os
from subprocess import call
from typing import *

'''
Squash a list of images into HDF5 without any label, unlike util.imageset.py
'''

## Parse command line
parser = argparse.ArgumentParser()
parser.add_argument('-l', type=str, action='store', dest='list',
                    required=True, help='image list txt file')
parser.add_argument('-o', type=str, action='store', dest='output',
                    default=__file__+'.h5', help='output hdf5 path')
parser.add_argument('-p', type=int, action='store', dest='pixels',
                    required=True, help='output image size')
parser.add_argument('-c', action='store_true', dest='c',
                    default=False, help='use HDF5 compression?')
parser.add_argument('-f', action='store_true', dest='force',
                    default=False, help='force overwrite the destination')
parser.add_argument('-v', action='store_true', dest='view',
                    default=False, help='show example image')
args = parser.parse_args()

## Configure
compargs = {'compression':'gzip', 'compression_opts':6} if args.c else {}

## Helpers
def readlist(_fpath):
    # -> list[ list[ str(path) ] ]
    with open(_fpath, 'r') as f:
        l = [ l.strip() for l in f.readlines() ]
    return l

def fillhdf5(_h5, _list, _group):
    for i, line in enumerate(_list, 1):
        print('\0337* {:3.1f}% | {}\0338'.format(i*100/len(_list), line), end='')
        if i < 10: print(repr(line))
        image = Image.open(line).resize((args.pixels, args.pixels), Image.BILINEAR)
        image = image.convert('RGB') # RGBA/... -> RGB
        if i == 1 and args.view: image.show()
        if i < 10: print('\t', image)
        # image -> [0,255], H,W,C
        image = np.asarray(image) # Image -> Numpy
        # HWC -> CHW
        image = image.transpose((2,0,1)) #image.swapaxes(0,2) roration:left:pi/4
        _h5[_group+'/images'][i-1,:,:,:] = image
        if i == 1 and args.view:
            Image.fromarray(_h5[_group+'/images'][i-1,:,:,:].transpose((1,2,0)), mode='RGB').show()

def createdsets(_h5, _list, _impath):
    # Chunks is crucial to compression performance
    # https://stackoverflow.com/questions/41771992/hdf5-adding-numpy-arrays-slow
    # https://stackoverflow.com/questions/16786428/compression-performance-related-to-chunk-size-in-hdf5-files
    # https://support.hdfgroup.org/HDF5/doc/Advanced/Chunking/Chunking_Tutorial_EOS13_2009.pdf
    h5.create_dataset(_impath, # N x C x H x W, np.ubyte (not np.byte! that will cause problem)
        (len(_list), 3, args.pixels, args.pixels), dtype=np.ubyte,
        chunks=(1, 3, args.pixels, args.pixels), **compargs)

# Read list files
imagelist = readlist(args.list)
print('-> Found {} images'.format(len(imagelist)))

# Create output file
if os.path.exists(args.output):
    if not args.force: raise SystemExit('HDF5 file {} already exists!'.format(args.output))
h5 = h5py.File(args.output, 'w')

# Fill HDF5
createdsets(h5, imagelist, '/images')
fillhdf5(h5, imagelist, '')
print(' *> processed {} images'.format(len(imagelist)))

# Write to disk
h5.close()
print('-> Dataset saved as {}'.format(args.output))
call(['sleep', '0.1'])
call(['h5ls', '-rv', args.output ])
