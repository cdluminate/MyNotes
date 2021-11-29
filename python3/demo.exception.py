#!/usr/bin/python3

import traceback
import sys

if len(sys.argv) < 2:
  raise Exception('missing argument')

class BrainDeadException(Exception):
  pass

try:
  raise BrainDeadException("oops")
except Exception as e:
  print(e)
