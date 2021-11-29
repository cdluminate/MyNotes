#!/usr/bin/python3

import pycurl
import sys
from multiprocessing.dummy import Pool

class Msg(object):
  def __init__(self):
    self.content = b''
  def callback(self, buf):
    self.content = self.content + buf

def scan_curl(target):
  msg = Msg()
  curl = pycurl.Curl()
  curl.setopt(pycurl.URL, bytes(target.encode()))
  curl.setopt(pycurl.TIMEOUT_MS, 70)
  curl.setopt(pycurl.WRITEFUNCTION, msg.callback)
  try:
    curl.perform()
  except pycurl.error as e:
    eid = e.args[0]
    message = e.args[1]
    if eid == 7: # Connection refused
      return 0
    elif eid == 28: # Connection timed out
      return 0
    else:
      print(target, eid, message)
      return 0
  if len(msg.content) > 0:
    print('{} : {}'.format(target, curl.getinfo(pycurl.HTTP_CODE)))
    print(msg.content.decode())
  sys.stdout.flush()
  sys.stderr.flush()
  return curl.getinfo(pycurl.HTTP_CODE)

if __name__ == '__main__':
  targets = []
  for i in range(1, 256):
    for j in range(1, 256):
      targets.append('10.170.{}.{}:22'.format(i,j))
  print("Scanning {} hosts ...".format(len(targets)))
  #list(map(scan_curl, targets)) # slow
  with Pool(32) as p:
    list(p.map(scan_curl, targets))
  print('Scan finished.')
