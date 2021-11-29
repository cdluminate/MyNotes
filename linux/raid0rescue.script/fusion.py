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
