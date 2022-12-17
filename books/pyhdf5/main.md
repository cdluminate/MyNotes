Python and HDF5
===

> Oreilly, Andrew Collete  

# Introduction

```python
import h5py
f = h5py.File("weather.hdf5")
f["/15/temperature"] = temperature
f["/15/temperature"].attrs["dt"] = 10.0
f["/15/temperature"].attrs["start_time"] = 1375204299
f["/15/wind"] = wind
f["/15/wind"].attrs["dt"] = 5.0
f["/20/temperature"] = temperature_from_station_20
```
This example illustrates two of the “killer features” of HDF5:
organization in hierarchical groups and attributes.
```
>>> dataset = f["/15/temperature"]
>>> for key, value in dataset.attrs.iteritems():
...     print "%s: %s" % (key, value)
```

# Getting Started

command lines tools
```
$ h5ls -vlr test.h5
$ h5dump test.h5
```

your first h5 file
```
# r: read-only, r+: read-write, w:overwrite, a:rw and create
f = h5py.File('test.hdf5', mode) # mode \in { w, r, r+, a }
f.close()
```

using context manager
```
with h5py.File('junk.hdf5', 'a') as f:
  ...
```

file drivers
```
# core driver is fast, entirely in memory
f = h5py.File('junk.hdf5', driver='core')

# family driver is designed for splitting up hdf5 into chunks
f = h5py.File("family.hdf5", driver="family", memb_size=1024**3) # 1 GiB

# mpio driver is for parallel computing
```

the user block
```
>>> f = h5py.File("userblock.hdf5", "w", userblock_size=512)
>>> f.userblock_size # Would be 0 if no user block present
512
>>> f.close()
>>> with open("userblock.hdf5", "rb+") as f:
...  f.write("a"*512)
```

# Working with datasets

basics
```
>>> arr = np.ones((5,2))
>>> f["my dataset"] = arr
>>> dset = f["my dataset"]
>>> dset
```

type and shape
```
>>> dset.dtype
dtype('float64')
>>> dset.shape
(5, 2)
```

reading and writing
```
# read the entire dataset
>>> out = dset[...]
>>> out
array([[ 1., 1.],
[ 1., 1.],
[ 1., 1.],
[ 1., 1.],
[ 1., 1.]])
>>> type(out)
<type 'numpy.ndarray'>

# writting to slice
>>> dset[1:4,1] = 2.0
>>> dset[...]
array([[ 1., 1.],
[ 1., 2.],
[ 1., 2.],
[ 1., 2.],
[ 1., 1.]])
```

create empty dataset, write some data to it, and sync
```
>>> dset = f.create_dataset("test1", (10, 10))
>>> dset
<HDF5 dataset "test1": shape (10, 10), type "<f4">
>>> dset = f.create_dataset("test2", (10, 10), dtype=np.complex64)
>>> dset
<HDF5 dataset "test2": shape (10, 10), type "<c8">

>>> dset = f.create_dataset("big dataset", (1024**3,), dtype=np.float32)

>>> dset[0:1024] = np.arange(1024)
>>> f.flush()
```

explicit storage type
```
>>> bigdata = np.ones((100,1000))
>>> bigdata.dtype
dtype('float64')
>>> bigdata.shape
(100, 1000)

>>> with h5py.File('big1.hdf5','w') as f1:
...  f1['big'] = bigdata

>>> with h5py.File('big2.hdf5','w') as f2:
...  f2.create_dataset('big', data=bigdata, dtype=np.float32)
```

automatic type conversion and direct reads
```
>>> dset = f2['big']
>>> dset.dtype
dtype('float32')
>>> dset.shape
(100, 1000)

>>> big_out = np.empty((100, 1000), dtype=np.float64)

>>> dset.read_direct(big_out)
```

reading with `astype`
```
>>> with dset.astype('float64'):
...  out = dset[0,:]
>>> out.dtype
dtype('float64')

>>> f.create_dataset('x', data=1e256, dtype=np.float64)
>>> print f['x'][...]
1e+256
>>> f.create_dataset('y', data=1e256, dtype=np.float32)
>>> print f['y'][...]
inf
```

reshaping
```
>>> imagedata.shape
(100, 480, 640)

>>> f.create_dataset('newshape', data=imagedata, shape=(100, 2, 240, 640))
```

fill values
```
>>> dset = f.create_dataset('empty', (2,2), dtype=np.int32)
>>> dset[...]
array([[0, 0],
[0, 0]])

>>> dset = f.create_dataset('filled', (2,2), dtype=np.int32, fillvalue=42)
>>> dset[...]
array([[42, 42],
[42, 42]])

>>> dset.fillvalue
42
```

reading and writing
```
>>> dset = f2['big']
>>> dset
<HDF5 dataset "big": shape (100, 1000), type "<f4">

# request a slice
>>> out = dset[0:10, 20:70]
>>> out.shape
(10, 50)

# Check for negative values and clip to 0
for ix in xrange(100):
  val = dset[ix,:] # Read one row
  val[ val < 0 ] = 0 # Clip negative values to 0
  dset[ix,:] = val # Write row back out
```

start-stop-step indexing
```
>>> dset = f.create_dataset('range', data=np.arange(10))
>>> dset[...]
array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> dset[4]
4
>>> dset[4:8]
array([4,5,6,7])
>>> dset[4:8:2]
array([4,6])

>>> dset[:]
array([0,1,2,3,4,5,6,7,8,9])

>>> dset[4:-1]
array([4,5,6,7,8])

# you can't inverse a vector in h5py like that in numpy
>>> a = np.arange(10)
>>> a
array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> a[::-1]
array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
>>> dset[::-1]
ValueError: Step must be >= 1 (got -1)
```

multidimentional and scalar slicing
```
>>> dset = f.create_dataset('4d', shape=(100, 80, 50, 20))
>>> dset[0,...,0].shape
(80, 50)

>>> dset[...].shape
(100, 80, 50, 20)

>>> dset = f.create_dataset('1d', shape=(1,), data=42)
>>> dset.shape
(1,)
>>> dset[0]
42
>>> dset[...]
array([42])

>>> dset = f.create_dataset('0d', data=42)
>>> dset.shape
()
>>> dset[0]
ValueError: Illegal slicing argument for scalar dataspace
>>> dset[...]
array(42)

>>> dset[()]
42
```

boolean indexing
```
>>> data = np.random.random(10)*2 - 1
>>> data
array([ 0.98885498, -0.28554781, -0.17157685, -0.05227003, 0.66211931,
0.45692186, 0.07123649, -0.40374417, 0.22059144, -0.82367672])
>>> dset = f.create_dataset('random', data=data)

>>> dset[data<0] = 0
>>> dset[...]
array([ 0.98885498, 0.45692186, 0.  , 0.07123649, 0.  0.  ,
, 0.  , 0.22059144, 0.66211931, 0.  ])

>>> dset[data<0] = -1*data[data<0]
>>> dset[...]
array([ 0.98885498, 0.28554781, 0.17157685, 0.05227003, 0.66211931,
0.45692186, 0.07123649, 0.40374417, 0.22059144, 0.82367672])
```

coordinate lists
```
>>> dset = f['range']
>>> dset[...]
array([0,1,2,3,4,5,6,7,8,9])

>>> dset[ [1,2,7] ]
array([1,2,7])
```

automatic broadcasting
```
>>> dset = f2['big']
>>> dset.shape
(100, 1000)

>>> data = dset[0,:]
>>> for idx in xrange(100):
...  dset[idx,:] = data

>>> dset[:,:] = dset[0,:]
```

reading directly to and existing array

*TODO: page 34*

# Chunking and Compression

TODO

compression filters
```
>>> dset = f.create_dataset("BigDataset",(1000,1000), dtype='f', compression="gzip")
>>> dset.compression
'gzip'
```

TODO

# Group, link, iteration

TODO
