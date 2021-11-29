#!/usr/bin/python3
from PIL import Image
import numpy as np
import h5py
import argparse
import random
import os
import sys
import subprocess
from subprocess import call
from typing import *
import pylab

'''
Convert a video into HDF5 frame by frame without any label, using FFmpeg.
Ref: http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/

## FFmpeg Tips

# FFmpeg cut video
https://superuser.com/questions/138331/using-ffmpeg-to-cut-up-video
  ffmpeg -ss 00:00:30.0 -i input.wmv -c copy -t 00:00:10.0 output.wmv
  ffmpeg -ss 30 -i input.wmv -c copy -t 10 output.wmv

# FFmpeg frame count
https://stackoverflow.com/questions/2017843/fetch-frame-count-with-ffmpeg
  ffprobe -i x.mp4 -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1
  ffprobe -i x.mp4 -v error -count_frames -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1
https://superuser.com/questions/84631/how-do-i-get-the-number-of-frames-in-a-video-on-the-linux-command-line
  ffprobe -i x.mp4 -show_streams -select_streams v:0

man ffmpeg | For extracting images from a video:
    ffmpeg -i foo.avi -r 1 -s WxH -f image2 foo-%03d.jpeg
'''

## Parse command line
parser = argparse.ArgumentParser()

parser.add_argument('-i', type=str, action='store', dest='input',
                    required=True, help='input video file')
parser.add_argument('--ih', type=int, action='store', dest='ih',
                    required=True, help='input height in pixel')
parser.add_argument('--iw', type=int, action='store', dest='iw',
                    required=True, help='input width in pixel')
parser.add_argument('--frames', type=int, action='store', dest='frames',
                    required=True, help='number of frames')

parser.add_argument('-o', type=str, action='store', dest='output',
                    default=__file__+'.h5', help='output hdf5 path')
parser.add_argument('--oh', type=int, action='store', dest='oh',
                    required=True, help='output height in pixel')
parser.add_argument('--ow', type=int, action='store', dest='ow',
                    required=True, help='output width in pixel')
parser.add_argument('-c', action='store_true', dest='c',
                    default=False, help='use HDF5 compression?')
parser.add_argument('-f', action='store_true', dest='force',
                    default=False, help='force overwrite the destination')

parser.add_argument('-d', action='store', dest='dir',
                    required=False, help='also dump some frames to dir')
parser.add_argument('-v', action='store_true', dest='view',
                    default=False, help='show example image')
parser.add_argument('--helpstub1', action='store_true', dest='help',
                    default=False, help='example usage:\n'+
'python3 util.imagesetvideo.py -i x.mp4 --ih 1080 --iw 1920 --frames 220 --oh 1080 --ow 1920 -c -f -d junk -o x.h5')
args = parser.parse_args()

## Configure
compargs = {'compression':'gzip', 'compression_opts':6} if args.c else {}
FFMPEG_BIN = 'ffmpeg'
FFMPEG_CMD = [ FFMPEG_BIN, '-v', 'error', '-i', args.input, '-f', 'image2pipe',
        '-pix_fmt', 'rgb24', '-vcodec', 'rawvideo', '-' ]

## Helpers
def createDataset(_h5, _N, _interpath):
    # Chunks is crucial to compression performance
    # https://stackoverflow.com/questions/41771992/hdf5-adding-numpy-arrays-slow
    # https://stackoverflow.com/questions/16786428/compression-performance-related-to-chunk-size-in-hdf5-files
    # https://support.hdfgroup.org/HDF5/doc/Advanced/Chunking/Chunking_Tutorial_EOS13_2009.pdf
    h5.create_dataset(_interpath, # N x C x H x W, np.ubyte (not np.byte!)
        (_N, 3, args.oh, args.ow), dtype=np.ubyte,
        chunks=(1, 3, args.oh, args.ow), **compargs)

def video2hdf5(_h5, _pipe, _dset):
    frmcount = 0
    while True:
        #    image = Image.open(line).resize((args.pixels, args.pixels), Image.BILINEAR)
        #    image = image.convert('RGB') # RGBA/... -> RGB
        #    if i == 1 and args.view: image.show()
        raw_image = _pipe.stdout.read(args.iw*args.ih*3) # [0,255], H,W,C
        if len(raw_image)==0: break
        frmcount += 1
        print('\0337* {:3.1f}% | {:07d}/{:d}\0338'.format(
            100*frmcount/args.frames, frmcount, args.frames), end='')
        sys.stdout.flush()
        image = np.fromstring(raw_image, dtype='uint8')
        #    image = np.asarray(image) # Image -> Numpy
        image = image.reshape((args.ih, args.iw, 3))
        if args.dir:
            if frmcount == 1 or frmcount == args.frames or random.random()>0.97:
                pylab.imshow(image)
                pylab.savefig(os.path.join(args.dir, 'f{}.png'.format(frmcount)))
        if frmcount <= args.frames:
            # HWC -> CHW
            # image = image.transpose((2,0,1)) #image.swapaxes(0,2) roration:left:pi/4
            image = image.transpose((2,0,1))
            _h5[_dset][frmcount-1,:,:,:] = image
        else:
            print('! omitting frame {}, length {}'.format(frmcount, len(raw_image)))
        #Image.fromarray(_h5[_group+'/images'][i-1,:,:,:].transpose((1,2,0)), mode='RGB').show()

# Test Input video
os.stat(args.input)
if not os.access(args.input, os.R_OK): raise SystemExit("specified file invalid")
print('-> Found video file {}'.format(args.input))

# Create output file
if os.path.exists(args.output):
    if not args.force: raise SystemExit('HDF5 file {} already exists!'.format(args.output))
h5 = h5py.File(args.output, 'w')
print('-> Created output hdf5 {}'.format(args.output))

# Open FFmpeg via pipe and Fill hdf5
createDataset(h5, args.frames, '/frames')
vp = subprocess.Popen(FFMPEG_CMD, stdout=subprocess.PIPE, bufsize=2**25)
print('-> Start convertion ...')
video2hdf5(h5, vp, '/frames')
print('-> Finalizing convertion ...')
h5.close() # must do this. Write to disk

# Final Check
print('-> Dataset saved as {}'.format(args.output))
call(['sleep', '0.1'])
call(['h5ls', '-rv', args.output ])
