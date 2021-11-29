#!/usr/bin/python3
# > http://docs.h5py.org/en/latest/quick.html

import logging as log
log.basicConfig(
  format='\x1b[36;1mL%(asctime)s %(process)d %(filename)s:%(lineno)d]'
    +' %(message)s\x1b[m',
  datefmt='%m%d %I:%M:%S',
  level=log.DEBUG
)

import h5py
import numpy as np

'''
Groups work like dictionaries, and datasets work like NumPy arrays
'''

log.info('create hdf5 file')
f = h5py.File ('tmpfile.hdf5', 'w')

log.info('create dataset')
dataset = f.create_dataset ('dataset', (100,), dtype='i')

log.info('assign data')
dataset[...] = np.arange(100)

log.info('dump database information')
print (dataset[1:10])
print (dataset.shape)
print (dataset.dtype)
print (dataset.size)
print (f.name)
print (dataset.name)

log.info('create groups')
group = f.create_group ('group')
dataset2 = group.create_dataset('another_dataset', (50,), dtype='f')
print (dataset2.name)
dataset3 = f.create_dataset('group2/data2', (10,), dtype='d')
print (dataset3.name)
dataset4 = f.create_dataset('compressed', (1000,1000), dtype='d',
        compression='gzip', compression_opts=1,
        data=np.random.randn(1000,1000))

log.info('retrieve data2')
data2 = f['group2/data2']
print (data2.name)

log.info('dump level 1 database entry')
for name in f:
    print (name)

log.info('dump all database entries')
f.visit(lambda x: print (x))
print (f.keys())

log.info('assign attribute')
dataset.attrs['temperature'] = 123.4

log.info('hard link')
f['hard/data1'] = f['dataset']
print (f['hard/data1'] == f['dataset'])

log.info('soft link')
f['soft/data1'] = h5py.SoftLink('/dataset')
print (f['soft/data1'] == f['/dataset'])

print()
log.info('re-reading hdf5 database')
f.close()
f = h5py.File ('tmpfile.hdf5', 'r')
dset = f.require_dataset ('dataset', (100,), dtype='i')
print (dset[1:10])

log.info('again, dump the tree of database')
f.visit(lambda x: print(x))
f.close()

log.info('demo end')

# _____________________________________________________________________________

log.info('generate src hdf5 file')
f = h5py.File ('junk.hdf5', 'w')

log.info('create data')
t_cnn   = np.random.random((16,1024))
t_lstm  = np.random.random((16,1024))
t_tree  = np.random.random((16,100))
t_label = np.random.random((16,100))

log.info('write data')
for i in range(1,2):
  f['/'+str(i)+'/cnn_embed'] = t_cnn
  f['/'+str(i)+'/lstm_embed'] = t_lstm
  f['/'+str(i)+'/tree_idx'] = t_tree
  f['/'+str(i)+'/label_idx'] = t_label

log.info('write string')
f['/strings/1'] = bytes('write a string to hdf5'.encode("utf8"))
f['/strings/2'] = 'another string into hdf5'

f.close()
log.info('done')

# _____________________________________________________________________________

f = h5py.File('junk.h5', 'w')
f.create_dataset('/string', (1,50), dtype='a25')
f.create_dataset('/u8', (1,50), dtype=np.int32)

f['/test'] = np.arange(10)
f['test2'] = np.ones(10, dtype=np.uint8)

f['/string'][0,0] = bytes('asdf'.encode('utf8'))
print(f['/string'])

f['/u8'][:] = np.ones((1,50), dtype=np.int32)
f['u8'][0,:4] = np.zeros((1,4), dtype=np.int32)
print(f['/u8'])

f['zhs'] = '你好' # simply works, implicitly using utf8
f['zhs2'] = '你好'.encode('utf8')
print( f['zhs2'][...].all().decode() )

f.close()

# ____________________________________________________________________________
'''
Inspecting the resulting hdf5, and repack hdf5 into compressed format.

    h5ls -r junk.h5
    h5ls -rfv junk.h5
    h5dump -g /strings junk.h5
    h5dump -d /strings/1 junk.h5
    h5dump -d features[493079,0;;1,40] junk.h5  # see man h5dump
    h5stat junk.h5
    h5repack -i junk.hdf5 -o junk.repack.h5 -f GZIP=9 -v

Further reading:

    http://cyrille.rossant.net/moving-away-hdf5/
    http://cyrille.rossant.net/should-you-use-hdf5/
'''

