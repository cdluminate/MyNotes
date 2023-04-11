'''
FlashLight: Personal PyTorch Helpers
Copyright (C) Mo Zhou
'''
from typing import *
import os
import _io
import gzip
import zstd
try:
    import ujson as json  # Fastest Json
except:
    import json


def jsonSave(obj: object, dest: Any) -> None:
    '''
    Serilize an object composed of List and Dict into file specified by
    path or io wrapper.
    '''
    if isinstance(dest, str):
        gz, zst = dest.endswith('.gz'), dest.endswith('.zst')
        if zst:
            with open(dest, 'wb') as f:
                f.write(zstd.dumps(json.dumps(obj).encode()))
        else:
            with (gzip.open(dest, 'wb') if gz else open(dest, 'w')) as f:
                f.write(json.dumps(obj).encode() if gz else json.dumps(obj))
    elif isinstance(dest, _io.TextIOWrapper) or isinstance(dest, _io.BufferedWriter):
        json.dump(obj, dest)
    else:
        raise TypeError(f'Unknown destination type {type(dest)}')


def jsonLoad(src: Any) -> Any:
    '''
    Load object from Json file handler, binary buffer, or file path.
    '''
    if isinstance(src, str):
        gz, zst = src.endswith('.gz'), src.endswith('.zst')
        if zst:
            with open(src, 'rb') as f:
                return json.loads(zstd.loads(f.read()))
        else:
            with (gzip.open(src, 'rb') if gz else open(src, 'r')) as f:
                return json.loads(f.read())
    else:
        return json.load(src)




def test_json_saveload_path(tmpdir):
    dest = str(tmpdir) + '/xxx'
    jsonSave([dest], dest)
    assert(dest == jsonLoad(dest)[0])
    os.remove(dest)


def test_json_saveload_pathgz(tmpdir):
    dest = str(tmpdir) + '/xxx.gz'
    jsonSave([dest], dest)
    assert(dest == jsonLoad(dest)[0])
    os.remove(dest)


def test_json_saveload_pathzst(tmpdir):
    dest = str(tmpdir) + '/xxx.zst'
    jsonSave([dest], dest)
    assert(dest == jsonLoad(dest)[0])
    os.remove(dest)


def test_json_saveload_fd(tmpdir):
    dest = str(tmpdir) + '/xxx'
    with open(dest, 'w') as f:
        jsonSave([dest], f)
    with open(dest, 'r') as f:
        assert(dest == jsonLoad(f)[0])
    os.remove(dest)
