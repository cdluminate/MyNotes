#!/usr/bin/env python3
# Show the structure of a given json file.
# Copyright © 2017 Lumin <cdluminate@gmail.com>
# MIT License

import json
import sys

class lsJson(object):

    def __init__(self, arg_indent_block='    '):
        '''
        configure
        '''
        self.s_indent_block = arg_indent_block
        self.__version__ = '3.1'

    def __call__(self, jobj, cdepth=0, show_example=False):
        '''
        wrapper call to self.lsjson
        '''
        self.lsjson(jobj, cdepth, show_example)

    @staticmethod
    def _c(s, color):
        ''' <helper>
        colorize the given string by wrapping it with ANSI color sequence
        in: s: given string
               color: string indicating the color
        out: str: colorized version of string s
        '''
        esc = '\x1b['
        restore = esc + ';m'
        if color=='red':
            c = esc+'31;1m' # red for list
        elif color=='green':
            c = esc+'32;1m' # green for int
        elif color=='yellow':
            c = esc+'33;1m' # yellow for dict
        elif color=='blue':
            c = esc+'34;1m' # blue for unknown
        elif color=='cyan':
            c = esc+'36;1m' # cyan for dict key
        elif color=='white':
            c = esc+'37;1m' # white for string
        elif color=='violet':
            c = esc+'35;1m' # for example and special use
        else:
            c = ''
        return c+s+restore

    @staticmethod
    def _type(obj):
        ''' <helper>
        alternative to built-in function type()
        in: obj
        out: string indicating the type of the given object
        '''
        if isinstance(obj, list):
            return 'List'
        elif isinstance(obj, dict):
            return 'Dict'
        elif isinstance(obj, bool):
            return 'Bol'
        elif isinstance(obj, int):
            return 'Int'
        elif isinstance(obj, str):
            return 'Str'
        elif isinstance(obj, float):
            return 'Flt'
        else:
            return str(type(obj))

    def lsjson(self, jobj, cdepth=0, show_example=False):
        ''' <main interface>
        Walk the json object (dict, list) recursively
        When the jobj is a list, we assume the inner structure
        of its elements is the same.
        in: jobj: any possible object found in json
            cdepth: current recursion depth, int
            show_example:
                -> True: show one example
                -> False: only dump structure
                -> 999: dump structure and all content
        '''
        #print(self.s_indent_block*cdepth, type(jobj), cdepth)
        if isinstance(jobj, list):
            if len(jobj)!=0: # non-empty list
                if show_example==999:
                    samples = jobj # dump all content
                else:
                    samples = [jobj[0]] # selectively dump the first
                print(self._c(self.s_indent_block*cdepth + '['+ str(self._type(jobj)), 'red'))
                for sample in samples:
                    lsjson(sample, cdepth=cdepth+1, show_example=show_example)
                if show_example==999:
                    print(self._c(self.s_indent_block*cdepth + ']', 'red'))
                else:
                    print(self._c(self.s_indent_block*cdepth + '... ]', 'red'))
            else:
                print(self._c(self.s_indent_block*cdepth + '[]', 'red'))
        elif isinstance(jobj, dict):
            if len(jobj.keys())!=0: # non-empty dict
                print(self._c(self.s_indent_block*cdepth + '{'+ str(self._type(jobj)), 'yellow'))
                for key in jobj.keys():
                    '''
                    if the sample is int or str, don't break line
                    '''
                    sample = jobj[key]
                    if isinstance(sample, int) or isinstance(sample, str):
                        endline = ''
                    else:
                        endline = '\n'
                    print(self._c(self.s_indent_block*(cdepth+1) + ':{:32s}'.format(key), 'cyan'), end=endline)
                    lsjson(sample, cdepth=cdepth+2, show_example=show_example)
                print(self._c(self.s_indent_block*cdepth + '}', 'yellow'))
            else:
                print(self._c(self.s_indent_block*cdepth + '{}', 'yellow'))
        elif isinstance(jobj, bool):
            print(self._c(self.s_indent_block*(9-cdepth)+str(self._type(jobj)), 'blue'))
            if show_example:
                print(self._c(self.s_indent_block*(cdepth-1) + '-> '+str(repr(jobj)), 'violet'))
        elif isinstance(jobj, int) or isinstance(jobj, float):
            print(self._c(self.s_indent_block*(9-cdepth)+str(self._type(jobj)), 'green'))
            if show_example:
                print(self._c(self.s_indent_block*(cdepth-1) + '-> '+str(repr(jobj)), 'violet'))
        elif isinstance(jobj, str):
            print(self._c(self.s_indent_block*(9-cdepth)+str(self._type(jobj)), 'white'))
            if show_example:
                print(self._c(self.s_indent_block*(cdepth-1) + '-> '+str(repr(jobj)), 'violet'))
        else:
            print(self._c(self.s_indent_block*cdepth+ str(self._type(jobj)), 'unknown'))

if __name__=='__main__':
    # configure
    b_show_example=False
    lsjson = lsJson()

    # helper
    def Usage():
        msg='''lsJson: pretty printer for json files
usage:
    lsjson <bla.json> [-e|-a]
flags:
    -e  show one example for each part of the structure
    -a  dump the structure and all the content
see also:
    json_pp in perl package, but lsjson is much prettier.
        '''
        print(msg)

    # argument check
    if len(sys.argv)==1:
        #raise Exception('where is input json file?')
        print(lsjson._c('where is input json file?', 'red'))
        Usage()
        exit(1)
    if len(sys.argv)==3 and sys.argv[2]=='-e': # show example
        b_show_example = True
    if len(sys.argv)==3 and sys.argv[2]=='-a': # dump all
        b_show_example = 999

    # main
    print(lsjson._c('=> lsjson '+sys.argv[1], 'violet'))
    try:
        j_content = json.loads(open(sys.argv[1], 'r').read())
        lsjson(j_content, show_example=b_show_example)
    except json.decoder.JSONDecodeError as e:
        print(lsjson._c('=> invalid or malformed file', 'red'))
        exit(2)
    except FileNotFoundError as e:
        print(lsjson._c('=> file not found', 'red'))
        exit(4) 
