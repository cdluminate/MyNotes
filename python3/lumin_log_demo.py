#!/usr/bin/python3
import lumin_log as log

def demo():
  log.debug('debug')
  log.info('info')
  log.warn('warn')
  log.error('error')
  log.fatal('fatal')
  
  log.error('error with function', True)

demo()
