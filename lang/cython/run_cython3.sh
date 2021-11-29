#!/bin/sh
# I don't like to use distutils for building cython lib.
# This wrapper is a working dirty hack.
set -e
test ! -z $1 || (echo "Error: Missing argv[1]"; false)
if test -z "$CC"; then export CC=gcc; fi

fpath=$1
fbare="$(echo $1 | sed -e 's/\.pyx$//')"
fbarebase=$(basename $fbare)
#echo $fpath, $fbare, $fbarebase

INCDIR=/usr/include/python3.6m/

echo "\033[31;1m> Compiling\033[m"
cython3 -3 $fpath  # Using Python3 syntax
$CC -shared -fPIC $fbare.c -o $fbare.so $CFLAGS $LDFLAGS -I$INCDIR -fopenmp

echo "\033[31;1m> Running\033[m"
python3 -c "import ${fbarebase}; $fbarebase.main()"

rm *.c *.so || true
