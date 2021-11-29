#!/bin/bash

python3 setup.py build

sofilename=$(basename `find . -name *.so | head -n1`)
sodirname=$(dirname `find . -name *.so | head -n1`)

export PYTHONPATH=$sodirname
echo $PYTHONPATH

python3 my_demo.py
