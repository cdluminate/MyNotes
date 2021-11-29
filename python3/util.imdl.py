#!/usr/bin/python3
import urllib.request
import os
import sys
from multiprocessing import Pool

'''
Image Downloader Code Template
Copyright (C) 2017 Lumin
'''

pool = 'pool'
imagelist = 'images.txt'

class Not200Exception(Exception):
    pass

def processLine(line):
    imagepath, imageurl = line.split()
    imagebasename, imagedirname = os.path.basename(imagepath), os.path.dirname(imagepath)

    # create directories if not exist
    if not os.path.exists(pool):
        os.mkdir(pool)
    if not os.path.exists(os.path.join(pool, imagedirname)):
        os.mkdir(os.path.join(pool, imagedirname))

    # pass is already downloaded
    if os.path.exists(os.path.join(pool, imagepath)):
        print('skipping', imagepath)
        return 0

    # download
    try:
        res = urllib.request.urlopen(imageurl)
        if res.status != 200:
            raise Not200Exception("http response is not 200")
    except Not200Exception as e:
        print(e)
        return 1
    except Exception as e:
        print(e)
        return 1

    # write to disk
    with open(os.path.join(pool, imagepath), 'wb') as outputfile:
        outputfile.write(res.read())
    print('->', imagepath, '... 200')
    sys.stdout.flush()
    return 0

with open(imagelist, 'r') as f:
    lines = f.readlines()
    with Pool(4) as p:
        res = list(p.map(processLine, lines))
