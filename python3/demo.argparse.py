#!/usr/bin/python3
'''
Argparse note
@reference: https://docs.python.org/3/howto/argparse.html
@reference: https://docs.python.org/3/library/argparse.html
'''
import argparse

def main(args):
  print(vars(args)) # https://stackoverflow.com/questions/16878315/what-is-the-right-way-to-treat-python-argparse-namespace-as-a-dictionary
  print('verbose: ', args.verbose)
  print('number : ', args.number)
  print('power  : ', args.power)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--verbose', help='toggle verbose mode', action='store_true')
  parser.add_argument('number', type=int, help='input a number')
  parser.add_argument('-p', '--power', help='power', type=int, default=1)
  args = parser.parse_args()
  main(args)
