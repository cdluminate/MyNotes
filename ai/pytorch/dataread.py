import torch as th
#th.multiprocessing.set_start_method('spawn')
import h5py
import numpy as np
import os
from torch.utils.data import dataset, sampler, DataLoader

maxepoch = 2

# [ Dataloader using in-memory dataset ]

x = th.rand(10, 8)
y = (th.rand(10, 1) * 10).int()
trainset = dataset.TensorDataset(x, y)
trainloader = DataLoader(trainset, batch_size=2,
        shuffle=True, num_workers=4, drop_last=True)

for epoch in range(maxepoch):
    for x in trainloader:
        print('1', x)

del x, y, trainset, trainloader

# [ Dataloader using hdf5 file + in-memory ]

# create fake dataset
if not os.path.exists(f'{__file__}.junk.h5'):
    h5 = h5py.File(f'{__file__}.junk.h5', 'w')
    h5.create_dataset('images', (10, 3, 224, 224),
            chunks=(10, 3, 224, 224), dtype=np.ubyte,
            compression='gzip', compression_opts=6)
    h5.create_dataset('labels', (10, 1),
            chunks=(10, 1), dtype=np.int,
            compression='gzip', compression_opts=6)
    h5['images'][:] = (np.random.rand(10, 3, 224, 224)*255).astype(np.ubyte)
    h5['labels'][:] = (np.random.rand(10, 1)*10).astype(np.int)
    h5.swmr_mode = True
    h5.close()
    del h5

h5 = h5py.File(f'{__file__}.junk.h5', 'r', swmr=True)
trainset = dataset.TensorDataset(th.from_numpy(h5['images'][:]), th.from_numpy(h5['labels'][:])) # does not save memory
print(trainset[0])
trainloader = DataLoader(trainset, batch_size=2,
        shuffle=True, num_workers=4, drop_last=True)

for epoch in range(maxepoch):
    for x in trainloader:
        print('2', x)

h5.close()
del h5, trainset, trainloader

# [ DataLoader using HDF5 ]
# when num_workers >= 2
# https://github.com/pytorch/pytorch/issues/3415
# http://docs.h5py.org/en/latest/swmr.html
# https://stackoverflow.com/questions/29251839/is-it-possible-to-do-parallel-reads-on-one-h5py-file-using-multiprocessing
# XXX: HDF5 read is still tricky at thread-safe read.
# XXX: what about parallel HDF5?
# NOTE: This is an I/O bound task instead of a CPU bound task.

class H5Dataset(dataset.Dataset):
    def __init__(self, data_dset, label_dset):
        '''
        data_dset, label_dset: HDF5 dataset
        '''
        assert(data_dset.shape[0] == label_dset.shape[0])
        self.data_dset = data_dset
        self.label_dset = label_dset
    def __getitem__(self, index):
        return th.from_numpy(self.data_dset[index]), \
            th.from_numpy(self.label_dset[index])
    def __len__(self):
        return self.data_dset.shape[0]

h5 = h5py.File(f'{__file__}.junk.h5', 'r', swmr=True)
trainset = H5Dataset(h5['images'], h5['labels'])
trainloader = DataLoader(trainset, batch_size=2, shuffle=False,
        num_workers=3, drop_last=True)

for epoch in range(maxepoch):
    for x in trainloader:
        print('3', x)

h5.close()
del h5, trainset, trainloader

# TODO: hdf5 file dataloader?
# TODO: image directory dataloader?
