'''
Ventilator, Worker, Sink
'''

import zmq
import random
import time
import sys


__SENDER__ = 'tcp://127.0.0.1:5557'
__SINK__   = 'tcp://127.0.0.1:5558'


def mainVentilator(argv):

    context = zmq.Context()

    sender = context.socket(zmq.PUSH)
    sender.bind(__SENDER__)

    sink = context.socket(zmq.PUSH)
    sink.connect(__SINK__)

    _ = input('> start?')

    print('Sink<-Vent:', 'start')
    sink.send(b'0')
    total_workload = 0
    for i in range(10):
        workload = random.random()
        total_workload += workload
        print('Work<-Vent:', workload)
        sender.send_string(f'{i}')

    print('total workload:', total_workload)
    time.sleep(1)


def mainWorker(argv):

    context = zmq.Context()

    recver = context.socket(zmq.PULL)
    recver.connect(__SENDER__)

    sender = context.socket(zmq.PUSH)
    sender.connect(__SINK__)

    while True:
        s = recver.recv()
        print('Vent->Work:', s)

        sys.stdout.write('.')
        sys.stdout.flush()

        time.sleep(float(s))
        print('Work->Sink:', 'signal')
        sender.send(b'')
        

def mainSink(argv):

    context = zmq.Context()

    recver = context.socket(zmq.PULL)
    recver.bind(__SINK__)

    s = recver.recv()
    print('->Sink:', s)

    tstart = time.time()
    for i in range(10):
        s = recver.recv()
        print('->Sink:', s)
        sys.stdout.write(':')
        sys.stdout.flush()
    tend = time.time()

    print('Time elapsed', tstart - tend)


if __name__ == '__main__':
    eval(f'main{sys.argv[1]}')(sys.argv[2:])
