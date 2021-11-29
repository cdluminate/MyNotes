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
