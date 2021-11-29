#!/usr/bin/python3
import lumin_log as log

def demo():
  log.info('lumin\'s rainbowlog demo in python')
  log.debug('debug')
  log.info('info')
  log.warn('warn')
  log.error('error')
  log.fatal('fatal')
  log.error('error report with function name', True)
  log.info('happy hacking!')

if __name__ == '__main__':
  demo()
