#!/usr/bin/python3
from PIL import Image
import numpy as np
import h5py
import argparse
import random
import os
from subprocess import call

#from torchvision import transforms
# TODO: read torchvision.transformations

'''
Convert an imageset from caffe list file to hdf5
See also: Caffe/convert_imageset
See also: Torchvision/tranformations
https://caffe2.ai/docs/tutorial-image-pre-processing.html
http://pytorch.org/tutorials/beginner/data_loading_tutorial.html
'''

## Parse command line
parser = argparse.ArgumentParser()
parser.add_argument('--trainlist', type=str, action='store', dest='trainlist',
                    required=True, help='image-label list file (train)')
parser.add_argument('--vallist', type=str, action='store', dest='vallist',
                    help='validation set list file')
parser.add_argument('--testlist', type=str, action='store', dest='testlist',
                    help='test set list file')
parser.add_argument('-o', type=str, action='store', dest='output',
                    default=__file__+'.h5', help='output hdf5 path')
parser.add_argument('-p', type=int, action='store', dest='pixels', # i.e. Scale
                    required=True, help='output image size')
parser.add_argument('-s', action='store_true', dest='s',
                    default=False, help='shuffle the list?')
parser.add_argument('-c', action='store_true', dest='c',
                    default=False, help='compression?')
parser.add_argument('-f', action='store_true', dest='force',
                    default=False, help='force overwrite output hdf5')
parser.add_argument('-v', action='store_true', dest='view',
                    default=False, help='view example image')
parser.add_argument('--div', action='store_true', dest='t_div', #TODO
                    default=False, help='transform: [0,255]->[0,1]?')
parser.add_argument('--normalize', action='store_true', dest='t_norm', # TODO
                    default=False, help='transform: chan = (chan - mean) / std)')
parser.add_argument('--centercrop', action='store_true', dest='t_ccrop', #TODO
                    default=False, help='transform: center crop')
args = parser.parse_args()

## Configure
compargs = {'compression':'gzip', 'compression_opts':6} if args.c else {}

## Helpers
def readlist(_fpath):
    # -> list[ list[ str(path), str(label) ] ]
    return [l.strip().split() for l in open(_fpath, 'r').readlines() ]

def fillhdf5(_h5, _list, _group):
    for i, line in enumerate(_list, 1):
        if i%100==0: print(' *> processed {} images'.format(i))
        path, label = line
        if i < 10: print(repr(path), repr(label))
        image = Image.open(path).resize((args.pixels, args.pixels), Image.BILINEAR)
        image = image.convert('RGB') # RGBA/... -> RGB
        if i == 1 and args.view: image.show()
        if i < 10: print('\t', image)
        # image -> [0,255], H,W,C
        image = np.asarray(image) # Image -> Numpy
        # HWC -> CHW
        image = image.transpose((2,0,1)) #image.swapaxes(0,2) roration:left:pi/4
        _h5[_group+'/images'][i-1,:,:,:] = image
        _h5[_group+'/labels'][i-1,:] = int(label)
        if i == 1 and args.view:
            Image.fromarray(_h5[_group+'/images'][i-1,:,:,:].transpose((1,2,0)), mode='RGB').show()

def createdsets(_h5, _list, _impath, _lbpath):
    # Chunks is crucial to compression performance
    # https://stackoverflow.com/questions/41771992/hdf5-adding-numpy-arrays-slow
    # https://stackoverflow.com/questions/16786428/compression-performance-related-to-chunk-size-in-hdf5-files
    # https://support.hdfgroup.org/HDF5/doc/Advanced/Chunking/Chunking_Tutorial_EOS13_2009.pdf
    h5.create_dataset(_impath, # N x C x H x W, np.ubyte (not np.byte! that will cause problem)
        (len(_list), 3, args.pixels, args.pixels), dtype=np.ubyte,
        chunks=(1, 3, args.pixels, args.pixels), **compargs)
    h5.create_dataset(_lbpath, # N x 1, int
        (len(_list), 1), dtype=np.int, chunks=(1,1), **compargs)

# Read list files
imagelist = readlist(args.trainlist)
if args.s: random.shuffle(imagelist)
print('-> Found {} images for training'.format(len(imagelist)))
if args.vallist:
    imagelist_vali = readlist(args.vallist)
    print('-> Found {} images for validation'.format(len(imagelist_vali)))
if args.testlist:
    imagelist_test = readlist(args.testlist)
    print('-> Found {} images for test'.format(len(imagelist_test)))

# Create output file
if os.path.exists(args.output):
    if not args.force: raise SystemExit('HDF5 file {} already exists!'.format(args.output))
h5 = h5py.File(args.output, 'w')

# Fill HDF5
createdsets(h5, imagelist, 'train/images', 'train/labels')
fillhdf5(h5, imagelist, 'train')
print(' *> processed {} images for training'.format(len(imagelist)))
if args.vallist:
    createdsets(h5, imagelist_vali, 'val/images', 'val/labels')
    fillhdf5(h5, imagelist_vali, 'val')
    print(' *> processed {} images for validation'.format(len(imagelist_vali)))
if args.testlist:
    createdsets(h5, imagelist_test, 'test/images', 'test/labels')
    fillhdf5(h5, imagelist_test, 'test')
    print(' *> processed {} images for validation'.format(len(imagelist_test)))

# Write to disk
h5.close()
print('-> Dataset saved as {}'.format(args.output))
call(['sleep', '0.1'])
call(['h5ls', '-rv', args.output ])
