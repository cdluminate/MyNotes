#!/usr/bin/python3
# Deflate your disk with useless bits to destroy any recoverable data
import os
import random
import sys

# configure
stripecount = 4096  # stripe count for each block
# 8192 - 16MiB
print('I: stripecount is {}'.format(stripecount))

# detect working directory
if not os.path.exists('deflating'):
    os.mkdir('deflating')

# prepare buffer
stripe = (bytes(hex(0x55).encode())+bytes(hex(0xAA).encode()))* 256  # this takes 512 Bytes
buffer = stripe * int(stripecount)

# start deflating
print('I: started deflating your disk')
combo = 0
while True:
    try:
        path = '{:0X}'.format(random.randint(0,256))
        needle = '{:0X}'.format(random.randint(0,256*256*256))
        # step1: create sub directory in need
        if not os.path.exists('deflating/{}'.format(path)):
            os.mkdir('deflating/{}'.format(path))
        # step2: detects existing stuff
        if os.path.exists('deflating/{}/{}'.format(path,needle)):
            print('I: skip -- will not overwrite existing file')
            continue
        # step3: create and defalte a new file
        with open('deflating/{}/{}'.format(path,needle), 'w+b') as f:
            f.write(buffer)
        combo += 1
        print('I: Junk file {} : {}-{}'.format(combo,path,needle))
        sys.stdout.flush()
    except Exception as e:
        print(e)
        exit()
