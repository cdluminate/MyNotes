#!/usr/bin/python3
'''
"Ridiculously simple network scanner with curl"
It scans for SSH host in specified network range.
'''
from multiprocessing import Manager
from multiprocessing.dummy import Pool
from subprocess import Popen, PIPE
from sys import stdout
from time import sleep

from spinloader import LoadSpinner, BarSpinner

class Spinner(object):
  def __init__(self):
    self.pool   = '-\\|/'
    self.cursor = 0
  def __call__(self):
    char = self.pool[self.cursor]
    self.cursor = self.cursor + 1
    if self.cursor >= len(self.pool):
      self.cursor = 0
    return char

def scan(target):
  cmd = [ 'curl', '-m', '0.05', '-s', target ]
  #print('scan:', ' '.join(cmd))
  proc = Popen(cmd, shell=False, stdout=PIPE)
  out, err = proc.communicate()
  if len(out) > 0:
    print('reply detected:', ' '.join(cmd))
    print(str(out.decode()))
  stdout.flush()

def scan6(target):
  cmd = [ 'curl', '-6', '-m', '0.05', '-s', target ]
  proc = Popen(cmd, shell=False, stdout=PIPE)
  out, err = proc.communicate()
  if len(out) > 0:
    print('caught reply:' ' '.join(cmd))
    print(str(out.decode()))
  stdout.flush()

def gentargets(port):
  targets = []
  base = '10.170.{}.{}:{}'
  for i in range(1,256):
    for j in range(1, 256):
      targets.append( base.format(i,j, port) )
  return targets

def gentargets6(port):
  targets = []
  base = '[2001:250:1006:dff0::{:x}:{:x}]:{}'
  for i in [1, 2, 3]:
    for j in range(65536):
      targets.append( base.format(i, j, port) )
  return targets

if __name__ == '__main__':
  with LoadSpinner('Scanning ... ', speed=LoadSpinner.FAST,
                    new_line=False, spinner=BarSpinner()) as ls:
    spinner = Spinner()
    #targets = gentargets(10022)
    targets = gentargets6(22)
    print('There are {} targets to scan.'.format(len(targets)))
    #stdout.write('Scanning ...  ')
    with Manager() as manager, Pool(12) as tp:
      #tpres = tp.map_async(scan, manager.list(targets))
      tpres = tp.map_async(scan6, manager.list(targets))
      while not tpres.ready():
        #print('\b'+spinner(), end='')
        sleep(0.1)
