RAID0 Rescue Experiement
===

> Copyright (C) 2016 Zhou Mo  
> MIT LICENSE (Expat)  

## Reference

`man mdadm`, `man md`

## Tools and Materials

`mdadm`, `coreutils`, `losetup`, `python3`, `Debian/Sid`

# Part1: Extract content from RAID0

In this part, a virtual RAID0 device which involves two physical drives
(emulated with loop device) will be set up with `mdadm`. This array
device will be formated as Ext4 filesystem. After filling some stuff
into the freshly created filesystem, the process of extracting a continuous
filesystem image from two scattered devices will be shown.

## Creating devices & array, Preparing filesystem

Create two disk images with `dd`:
```
$ dd if=/dev/zero of=vda.img bs=16M count=1
$ dd if=/dev/zero of=vdb.img bs=16M count=1
```
Emulate physical device with the help of loop:
```
# modprobe loop
# losetup -f ./vda.img
# losetup -f ./vdb.img
```
See? there are new devices:
```
$ lsblk
loop0    7:0    0    16M  0 loop 
loop1    7:1    0    16M  0 loop 
```
Let's consider these two loop devices as real disks.  
Then we create software raid:
```
$ sudo mdadm -C /dev/md0 -a yes -l0 -n2 /dev/loop0 /dev/loop1
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md0 started.
$ lsblk
loop0    7:0    0    16M  0 loop  
└─md0    9:0    0    30M  0 raid0 
loop1    7:1    0    16M  0 loop  
└─md0    9:0    0    30M  0 raid0 
```
Next, we create Ext4 filesystem on this device:
```
$ sudo mkfs.ext4 /dev/md0
```
Let's mount it and put something in:
```
$ sudo mount /dev/md0 /mnt
$ sudo cp ../gnome-backgrounds-3.16.0.tar.xz /mnt/
$ md5sum ../gnome-backgrounds-3.16.0.tar.xz 
eeb8a369f5f0c5daca0bb57c88acfbdf  ../gnome-backgrounds-3.16.0.tar.xz
$ sha1sum ../gnome-backgrounds-3.16.0.tar.xz 
0a33b77dd087a53168853861702ce3bba4bf994d  ../gnome-backgrounds-3.16.0.tar.xz
```
Let's gather some information:
```
$ sudo mdadm -QD /dev/md0
/dev/md0:
        Version : 1.2
  Creation Time : Tue Aug 30 16:09:04 2016
     Raid Level : raid0
     Array Size : 30720 (30.00 MiB 31.46 MB)
   Raid Devices : 2
  Total Devices : 2
    Persistence : Superblock is persistent

    Update Time : Tue Aug 30 16:09:04 2016
          State : clean 
 Active Devices : 2
Working Devices : 2
 Failed Devices : 0
  Spare Devices : 0

     Chunk Size : 512K

           Name : Sid:0  (local to host Sid)
           UUID : f51ef1ef:35724284:b44796fd:5134bcdc
         Events : 0

    Number   Major   Minor   RaidDevice State
       0       7        0        0      active sync   /dev/loop0
       1       7        1        1      active sync   /dev/loop1
$ sudo mdadm -Evvvvs /dev/loop0
/dev/loop0:
          Magic : a92b4efc
        Version : 1.2
    Feature Map : 0x0
     Array UUID : f51ef1ef:35724284:b44796fd:5134bcdc
           Name : Sid:0  (local to host Sid)
  Creation Time : Tue Aug 30 16:09:04 2016
     Raid Level : raid0
   Raid Devices : 2

 Avail Dev Size : 30720 (15.00 MiB 15.73 MB)
    Data Offset : 2048 sectors
   Super Offset : 8 sectors
   Unused Space : before=1960 sectors, after=0 sectors
          State : clean
    Device UUID : 7484c902:87fbb018:ebf545c3:00365379

    Update Time : Tue Aug 30 16:09:04 2016
  Bad Block Log : 512 entries available at offset 72 sectors
       Checksum : 39be55ad - correct
         Events : 0

     Chunk Size : 512K

   Device Role : Active device 0
   Array State : AA ('A' == active, '.' == missing, 'R' == replacing)
```
Well, now we can unmount this filesystem and stop this array.
```
$ sudo umount /mnt
$ sudo mdadm -S /dev/md0
mdadm: stopped /dev/md0
$ sudo losetup -D /dev/loop0
$ sudo losetup -D /dev/loop1
```

## Extract filesystem into an image

TODO: explain why and how does this script work.

```python3
#!/usr/bin/python3
# Copyright (C) Zhou Mo
# MIT LICENSE (Expat)
import os
import sys

'''
This script fusions two raid0 disk images into one.
DiskArray: Linux Mdadm, RAID0, with superblocks
'''

diskA = './vda.img'
diskB = './vdb.img'
diskAB = './vdab.img'

print ('RAID0 Fusion ...')
with open(diskA, 'rb') as sda, open(diskB, 'rb') as sdb, open(diskAB, 'w+b') as sdab:
  try:
    # skip superblock
    sda.seek(2048*512)
    sdb.seek(2048*512)
    # read and assemble
    while(True):
      bufA = sda.read(512*1024) # Stripe: 512KB
      bufB = sdb.read(512*1024)
      if len(bufA) == 0 and len(bufB) == 0: break
      bufAB = bufA + bufB
      sdab.write(bufAB)
  except Exception as e:
    print(e)

print (' ok')
```

We run the above python script and see the result
```
$ python3 fusion.py 
RAID0 Fusion ...
 ok
$ ls -lhS
total 47M
-rw-r--r-- 1 lumin lumin  30M Aug 30 16:18 vdab.img  <-- New file
-rw-r--r-- 1 lumin lumin  16M Aug 30 16:15 vda.img
-rw-r--r-- 1 lumin lumin  16M Aug 30 16:11 vdb.img
-rw-r--r-- 1 lumin lumin 1.1K Aug 30 15:53 parity.py
-rw-r--r-- 1 lumin lumin  721 Aug 30 15:31 fusion.py
```
The generated file is indeed invalid filesystem image:
```
$ sudo mount ./vdab.img /mnt
$ md5sum /mnt/*
eeb8a369f5f0c5daca0bb57c88acfbdf  /mnt/gnome-backgrounds-3.16.0.tar.xz
$ sha1sum /mnt/*
0a33b77dd087a53168853861702ce3bba4bf994d  /mnt/gnome-backgrounds-3.16.0.tar.xz
```

Everything seems to be fine.

# Part2: Manual Parity for RAID0

In this part, with the two disk images created in the previous part
a parity image is created. Then, the disk image A is restored from disk
image B and the parity image in case of disk image A being removed.

## Preparation

We need the hashsums of our disk images:
```
$ md5sum *
6e21eec52203ddf6bed6cbb95d526608  vda.img
bc27dff86bdba7a5e003588077208064  vdb.img
```

## Create Parity Image

TODO: explain why and how does the script work.  
with this script
```python
#!/usr/bin/python3
# Copyright (C) Zhou Mo
import os
import sys

'''
This script calculates the parity of two files
'''

if len(sys.argv) != 4:
  raise Exception("Argument!")
if len(sys.argv[1])==0 or len(sys.argv[2])==0:
  raise Exception("where is your disk images?")
if len(sys.argv[3])==0:
  raise Exception("where should I write the parity image?")

def parity(chunkA, chunkB):
  if type(chunkA)!=bytes or type(chunkB)!=bytes:
    raise Exception("Invalid input")
  if len(chunkA) != len(chunkB):
    raise Exception("Input lengths don't match")
  a = list(map(int, chunkA))
  b = list(map(int, chunkB))
  c = list(map(lambda pack: pack[0]^pack[1], zip(a, b)))
  return bytes(c)

print ('Manual Parity ...')
with open(sys.argv[1], 'rb') as sda, open(sys.argv[2], 'rb') as sdb, open(sys.argv[3], 'w+b') as sdc:
  try:
    # read and parity
    while(True):
      bufA = sda.read(512*1024) # Stripe: 512KB
      bufB = sdb.read(512*1024)
      if len(bufA) == 0 and len(bufB) == 0: break
      sdc.write(parity(bufA, bufB))
  except Exception as e:
    print(e)

print (' ok, see file {}'.format(sys.argv[3]))
```

Let's create the parity image with the above script
```
$ python3 parity.py vda.img vdb.img pq.img
Manual Parity ...
 ok, see file pq.img
$ md5sum *
3fcf96dd0216a8f135ef18cd1fe6602b  pq.img
6e21eec52203ddf6bed6cbb95d526608  vda.img
bc27dff86bdba7a5e003588077208064  vdb.img
```

And I'm quite happy removing my disk image `vda.img`:
```
$ shred -u vda.img
```

Oh wait, what have I done? I removed my data! Let's rescue it:
```
$ python3 parity.py vdb.img pq.img vda_restore.img
Manual Parity ...
 ok, see file vda_restore.img
$ md5sum *
bd5a635b7fd07e1b8596e61411807a69  fusion.py
aee41c9ccad6d74c1d6e4d60bca2425b  parity.py
3fcf96dd0216a8f135ef18cd1fe6602b  pq.img
6e21eec52203ddf6bed6cbb95d526608  vda_restore.img
bc27dff86bdba7a5e003588077208064  vdb.img
```
Have you noticed that the resulting `vda_restore.img` shares the same
md5sum with the original `vda.img`?
