import torch as th
import torchvision as vision
import h5py
import numpy as np
import os

# create fake dataset
if not os.path.exists('junk.h5'):
    h5 = h5py.File('junk.h5', 'w')
    h5.create_dataset('images', (10, 3, 224, 224),
            chunks=(10, 3, 224, 224), dtype=np.ubyte,
            compression='gzip', compression_opts=6)
    h5['images'][:] = (np.random.rand(10, 3, 224, 224)*255).astype(np.ubyte)
    h5.close()
    del h5

h5 = h5py.File('junk.h5', 'r')
batchin = th.autograd.Variable(th.from_numpy(h5['images'][:])).float()
print(batchin.shape)
cnn = vision.models.resnet18(True) # pre-trained
batchout = cnn(batchin)
print(batchout.shape)

h5.close()

# TODO: larger hdf5 feature extraction?
# TODO: image folder feature extraction?
