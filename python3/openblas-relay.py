#!/usr/bin/python3
'''
OpenBLAS Relay Library Generator
Copyright (C) 2019 Mo Zhou <lumin@debian.org>
License: MIT/Expat

Julia decided to mangle the symbols of the vendored copy of openblas
(INTERFACE64=1). I didn't read all the past discussions but in fact the symbol
mangling introduced difficulty in distribution packaging, and the mangling rule
is not standarlized yet.

I'm been updating the whole BLAS/LAPACK ecosystem on Debian(Ubuntu) since long
time ago. Our original plan was to provide libopenblas64.so without symbol
mangling, because MKL doesn't mangle the symbols and we expect every
BLAS/LAPACK implementation could be used as a drop-in replacement in the
system.

To provide support for Julia's libopenblas64_.so, indeed we could compile
src:openblas again with slightly different configuration, but then we will have
to build it 7 times (32/64-bit indexing * serial,pthread,openmp). And the
one compiled for Julia will be almost a duplicated one.

I'm trying to generate a "relay" library to provide ABIs like "sgemm_64_" which
immediately calls the "sgemm_" from libopenblas64.so (no mangling). The "relay"
library can be compiled as "libopenblas64_.so.0" with a correcponding SONAME,
and linked against "libopenblas64.so.0". So we can reuse a existing
64-bit-indexing openblas.

With slight tweaks, this library can also work with MKL.
'''

import re
import sys
import os
import argparse


def read_mkl_headers(dirname: str = '/usr/include/mkl') -> dict:
    '''
    Read the MKL header files: mkl_{,c}blas.h, mkl_lapack{,e}.h
    '''
    headers = {}
    for key in ('mkl_blas', 'mkl_cblas', 'mkl_lapack', 'mkl_lapacke'):
        with open(os.path.join(dirname, key + '.h'), 'rt') as f:
            headers[key] = f.read()
    return headers


def generate_relay_lib(headers: dict = {}, opts: dict = {}) -> str:
    '''
    Generate the Relay Library C Code
    '''
    lib = []
    lib.extend(f'''
typedef struct _complex8 {{ float* real; float* imag; }} complex8;
typedef struct _complex16 {{ double* real; double* imag; }} complex16;

typedef {opts['int']} (*C_SELECT_FUNCTION_1) ( const complex8* );
typedef {opts['int']} (*C_SELECT_FUNCTION_2) ( const complex8*, const complex8* );
typedef {opts['int']} (*D_SELECT_FUNCTION_2) ( const double*, const double* );
typedef {opts['int']} (*D_SELECT_FUNCTION_3) ( const double*, const double*, const double* );
typedef {opts['int']} (*S_SELECT_FUNCTION_2) ( const float*, const float* );
typedef {opts['int']} (*S_SELECT_FUNCTION_3) ( const float*, const float*, const float* );
typedef {opts['int']} (*Z_SELECT_FUNCTION_1) ( const complex16* );
typedef {opts['int']} (*Z_SELECT_FUNCTION_2) ( const complex16*, const complex16* );

void openblas_set_num_threads64_(int num_threads) {{ openblas_set_num_threads(num_threads); }};
int openblas_get_num_threads64_(void)             {{ openblas_get_num_threads(); }};
int openblas_get_num_procs64_(void)               {{ openblas_get_num_procs(); }};
char* openblas_get_config64_(void)                {{ openblas_get_config(); }};
char* openblas_get_corename64_(void)              {{ openblas_get_corename(); }};
int openblas_get_parallel64_(void)                {{ openblas_get_parallel(); }};
            '''.split('\n'))
    if 'blas' in opts['abi'].split(','):
        for api in re.findall('\w+?\s+[sdczlix][a-z0-9]+\(.*?\)\s*;',
                              headers['mkl_blas'], flags=re.DOTALL):
            if '#' in api:
                continue
            api = ' '.join(api.replace('\n', ' ').split())
            api = re.sub('MKL_INT', opts['int'], api)
            api = re.sub('MKL_Complex8', 'complex8', api)
            api = re.sub('MKL_Complex16', 'complex16', api)
            tp, name, args = re.match(
                r'(\w+?)\s+([sdczlix][a-z0-9]+)\((.*?)\)\s*;', api).groups()
            argnames = ', '.join([x.split()[-1].replace('*', '')
                                  for x in args.split(',')])
            lib.extend(f'''
{tp} {name+'_'+opts['dmangle']} (
    {args})
{{
    {'return' if 'void'!=tp else ''} {name+'_'+opts['smangle']}({argnames});
}};
                    '''.split('\n'))
            print(
                'RELAY',
                name +
                '_' +
                opts['smangle'],
                '->',
                name +
                '_' +
                opts['dmangle'],
                '(',
                argnames,
                ')')
    if 'cblas' in opts['abi'].split(','):
        raise NotImplementedError
    if 'lapack' in opts['abi'].split(','):
        for api in re.findall('\w+?\s+[sdcz][a-z0-9]+_\(.*?\)\s*;',
                              headers['mkl_lapack'], flags=re.DOTALL):
            api = ' '.join(api.replace('\n', ' ').split())
            api = re.sub('MKL_INT', opts['int'], api)
            api = re.sub('MKL_Complex8', 'complex8', api)
            api = re.sub('MKL_Complex16', 'complex16', api)
            api = re.sub('MKL_', '', api)
            tp, name, args = re.match(
                r'(\w+?)\s+([sdcz][a-z0-9]+_)\((.*?)\)\s*;', api).groups()
            argnames = ', '.join([x.split()[-1].replace('*', '')
                                  for x in args.split(',')])
            argnames = '' if argnames == 'void' else argnames
            lib.extend(f'''
{tp} {name+opts['dmangle']} (
    {args})
{{
    {'return' if 'void'!=tp else ''} {name+opts['smangle']}({argnames});
}};
                    '''.split('\n'))
            print('RELAY', name +
                  opts['smangle'], '->', name +
                  opts['dmangle'], '(', argnames, ')')
    if 'lapacke' in opts['abi'].split(','):
        raise NotImplementedError
    return '\n'.join(lib)


if __name__ == '__main__':
    # parse arguments
    ag = argparse.ArgumentParser()
    ag.add_argument('-A', '--abi', type=str, default='blas,lapack',
                    help='Set of ABIs that the relay library should provide')
    ag.add_argument('-o', '--output', type=str, default='./openblas-relay.c')
    ag.add_argument('--mkl', type=str, default='/usr/include/mkl')
    ag.add_argument('--int', type=str, default='long')
    ag.add_argument('--smangle', type=str, default='',
                    help='Mangle the source symbol')
    ag.add_argument('--dmangle', type=str, default='64_',
                    help='Mangle the destination symbol')
    ag = vars(ag.parse_args(sys.argv[1:]))
    # generate the library
    headers = read_mkl_headers(ag['mkl'])
    with open(ag['output'], 'wt') as f:
        f.write(generate_relay_lib(headers, ag))
    os.system('gcc -flto -O2 -g -shared -fPIC openblas-relay.c -o libopenblas64_.so.0 -L. -lopenblas64 -Wno-implicit-function-declaration -Wl,-soname -Wl,libopenblas64_.so.0')
    os.unlink('openblas-relay.c')
