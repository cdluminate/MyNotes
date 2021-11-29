#!/usr/bin/python3
# lumin's logging library, imitating Google's Glog, behaves as a lite
# version of Glog, but some new features are introduced.
# Copyright (c) 2016 Zhou Mo <cdluminate AT gmail DOT com>
# MIT License
# @reference python's standard library source file Lib/logging/__init__.py

import sys
import os
import time

# configuration
default_logging_fd = 2

# Important initialization
# this is borrowed from the standard library 'logging'
if hasattr(sys, '_getframe'):
  currentframe = lambda: sys._getframe(3)
else: #pragma: no cover
  def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
      raise Exception
    except Exception:
      return sys.exc_info()[2].tb_frame.f_back

# helper functions
def _lumin_get_MMDDHHMMSSms():
  gmtime = time.gmtime()
  MM = gmtime.tm_mon
  DD = gmtime.tm_mday
  HH = gmtime.tm_hour
  mm = gmtime.tm_min
  SS = gmtime.tm_sec
  ms = '%.5f'%(time.time())
  ms = str(ms).split('.')[1]
  return '%02d%02d %02d:%02d:%02d.%s'%(MM, DD, HH, mm, SS, ms)

def _lumin_log_core(fn, lno, func, pfunc=False):
  MMDD_HHMMSSms = _lumin_get_MMDDHHMMSSms()
  PID = os.getpid()
  if pfunc == False:
    ret = '%s %s %s:%s] '%(MMDD_HHMMSSms, PID, fn, lno)
  else:
    ret = '%s %s %s:%s] @%s() '%(MMDD_HHMMSSms, PID, fn, lno, func)
  return ret

# logging functions
def debug(message, pfunc=False):
  try:
    f = sys._getframe()
    fn = f.f_back.f_code.co_filename
    lno = f.f_back.f_lineno
    func = f.f_back.f_code.co_name
  except ValueError: # pragma: no cover
    fn, lno, func = "(unknown file)", 0, "(unknown function)"
  output = '\x1b[36;1mD' + _lumin_log_core(fn, lno, func, pfunc) + message + '\x1b[m\n'
  os.write(2, bytes(output.encode()))

def info(message, pfunc=False):
  try:
    f = sys._getframe()
    fn = f.f_back.f_code.co_filename
    lno = f.f_back.f_lineno
    func = f.f_back.f_code.co_name
  except ValueError: # pragma: no cover
    fn, lno, func = "(unknown file)", 0, "(unknown function)"
  output = '\x1b[32;1mI' + _lumin_log_core(fn, lno, func, pfunc) + message + '\x1b[m\n'
  os.write(2, bytes(output.encode()))

def warn(message, pfunc=False):
  try:
    f = sys._getframe()
    fn = f.f_back.f_code.co_filename
    lno = f.f_back.f_lineno
    func = f.f_back.f_code.co_name
  except ValueError: # pragma: no cover
    fn, lno, func = "(unknown file)", 0, "(unknown function)"
  output = '\x1b[33;1mW' + _lumin_log_core(fn, lno, func, pfunc) + message + '\x1b[m\n'
  os.write(2, bytes(output.encode()))

def error(message, pfunc=False):
  try:
    f = sys._getframe()
    fn = f.f_back.f_code.co_filename
    lno = f.f_back.f_lineno
    func = f.f_back.f_code.co_name
  except ValueError: # pragma: no cover
    fn, lno, func = "(unknown file)", 0, "(unknown function)"
  output = '\x1b[31;1mE' + _lumin_log_core(fn, lno, func, pfunc) + message + '\x1b[m\n'
  os.write(2, bytes(output.encode()))

def fatal(message, pfunc=False):
  try:
    f = sys._getframe()
    fn = f.f_back.f_code.co_filename
    lno = f.f_back.f_lineno
    func = f.f_back.f_code.co_name
  except ValueError: # pragma: no cover
    fn, lno, func = "(unknown file)", 0, "(unknown function)"
  output = '\x1b[35;1mF' + _lumin_log_core(fn, lno, func, pfunc) + message + '\x1b[m\n'
  os.write(2, bytes(output.encode()))

