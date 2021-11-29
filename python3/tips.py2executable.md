Python code to executable
===

https://stackoverflow.com/questions/5458048/how-to-make-a-python-script-standalone-executable-to-run-without-any-dependency

```
pip3 install pyinstaller # cross platform
py2exe # only windows
cython
```

Compile private modules with cython, and package the source files
into an executable with pyinstaller.

```
cython3 a.py -lpython3.5 -I/usr/include/python3.5
pyinstaller a.py
```
