'''
A request-reply model.
  REQ     REP

they connect to each other.
'''
import sys
import time
import zmq
from zmq.utils import jsonapi
from tqdm import tqdm
import argparse
import random


__ADDRESS__ = 'tcp://127.0.0.1:5555'


def mainServer(argv):

    ag = argparse.ArgumentParser()
    ag.add_argument('-v', '--verbose', action='store_true')
    ag = ag.parse_args(argv)

    socket = zmq.Context().socket(zmq.REP)
    socket.bind(__ADDRESS__)

    for _ in tqdm(iter(int, 1)):
        msg = jsonapi.loads(socket.recv())
        if ag.verbose: print('->', msg)
        rep = {'type': 'response', 'id': msg['id']}
        if ag.verbose: print('<-', rep)
        socket.send(jsonapi.dumps(rep))


def mainClient(argv):

    ag = argparse.ArgumentParser()
    ag.add_argument('-n', '--num', type=int, default=10000)
    ag.add_argument('-v', '--verbose', action='store_true')
    ag.add_argument('-i', '--interval', type=float, default=0.)
    ag = ag.parse_args(argv)

    socket = zmq.Context().socket(zmq.REQ)
    socket.connect(__ADDRESS__)

    for i in tqdm(range(ag.num) if ag.num>0 else iter(int, 1)):
        req = {'type': 'request', 'id': random.random()}
        if ag.verbose: print('<-', req)
        socket.send(jsonapi.dumps(req))
        msg = jsonapi.loads(socket.recv())
        if msg['id'] != req['id']:
            print('Warning: id mismatch!')
        if ag.verbose: print('->', msg)
        if ag.interval != 0.0: time.sleep(ag.interval)


if __name__ == '__main__':
    print('libzmq', zmq.zmq_version(), 'pyzmq', zmq.__version__)
    eval(f'main{sys.argv[1]}')(sys.argv[2:])
