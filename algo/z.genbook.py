#!/usr/bin/python3
import os
import sys
import glob
from pprint import pprint
import shlex
from subprocess import call
from time import ctime

rstbook = []
rstbook.append("""
========================
Auto-Generated Code Book
========================

:Author: Lumin 
:Date:   {}

Preface
=======

This book Contains some of my algorithm *snippets*, some *LeetCode*
solutions and some *Project Euler* solutions. Programming languages
used in this book are ``C++``, ``Python``, ``Julia``, ``Lua`` and ``Go``.

The files named ``z.<name>.<suffix>`` are my snippets.
Files with name ``<number>.lc.<name>.<suffix>`` are leetcode solutions.
Similarly, mark ``su`` stands for solution euler.

I use ``O()`` notation for time complexity. Sometimes I use ``S()``
for spatial complexity.

Algorithms
----------

Reference *Anany Levitin Introduction to the design and analysis of algorighms*

several important types of problems

#. sorting problem
#. searching problem
#. string problem
#. graph and network
#. combination and permutation
#. geonetric algorithm
#. numerical problem

fundamental data structures

#. linear data structures
  #. array
  #. string
  #. linked list
  #. doubly linked list
  #. stack
  #. queue
#. graph
  #. undirected graph
  #. directed graph
  #. weighted graph
#. tree
  #. rooted tree
  #. ordered tree
#. set and dictionary

Leetcode solution references
----------------------------

#. https://github.com/soulmachine/leetcode

#. http://bookshadow.com/leetcode/

#. https://www.gitbook.com/book/siddontang/leetcode-solution/details

::

  Copyright (C) 2017 Lumin <cdluminate@gmail.com>
  MIT LICENSE

""".format(ctime()))

# -- Glob all sources
files = glob.glob('**')
# remove myself
files.pop(files.index(__file__))
print('=> Found {} files'.format(len(files)))
#pprint(files)

# -- Collect files into categories
def collectbysuffix(suffix, flist):
    matches = [ f for f in flist if f.endswith(suffix) ]
    matches.sort()
    return matches

cppfiles = collectbysuffix('.cc', files) \
         + collectbysuffix('.hpp', files)
print(' -> {} cpp files'.format(len(cppfiles)))
pyfiles  = collectbysuffix('.py', files)
print(' -> {} py files'.format(len(pyfiles)))
jlfiles  = collectbysuffix('.jl', files)
print(' -> {} jl files'.format(len(jlfiles)))
gofiles  = collectbysuffix('.go', files)
print(' -> {} go files'.format(len(gofiles)))
luafiles  = collectbysuffix('.lua', files)
print(' -> {} lua files'.format(len(luafiles)))
rustfiles = collectbysuffix('.rs', files)
print(' -> {} rust files'.format(len(rustfiles)))

# -- write statistics
rstbook.append("""

Statistics
----------

::

  * C++    source files: {}
  * Python source files: {}
  * Julia  source files: {}
  * Go     source files: {}
  * Lua    source files: {}
  * Rust   source files: {}
""".format( len(cppfiles), len(pyfiles), len(jlfiles), len(gofiles), len(luafiles), len(rustfiles) ))

# -- generate sections
def genSection(rstbook, title, flist, ftype):
    # section header
    rstbook.append("""
{}
{}
""".format(title, '='*len(title)))
    # add files
    for i, f in enumerate(flist, 1):
        rstbook.append("""
{}. ``{}``
{}

.. code:: {}

""".format(i, f, '-'*( len(str(i)) + len(f) + 6 ), ftype))
        fo = open(f, 'r')
        for line in fo.readlines():
            rstbook.append('  ' + line)
        fo.close()

genSection(rstbook, "C++ Part", cppfiles, "cpp")
genSection(rstbook, "Python Part", pyfiles, "python")
genSection(rstbook, "Julia Part", jlfiles, "julia")
genSection(rstbook, "Go Part", gofiles, "go")
genSection(rstbook, "Lua Part", luafiles, "lua")
genSection(rstbook, "Rust Part", rustfiles, "rust")

# -- save, convert, cleanup
with open(__file__ + '.rst', 'w+') as f:
    f.writelines(rstbook)
print('=> Saved. Start to generate pdf ...')
cmd_pandoc = 'pandoc -f rst -t latex {}.rst -o {}.pdf'.format(
        __file__, __file__) + " -V mainfont=times" + \
        " -V geometry=margin=1in --toc -V toccolor=magenta"
cmd_cleanup = 'rm {}.rst'.format(__file__)
print(' -> pandoc ...')
call(shlex.split(cmd_pandoc))
print(' -> clean up ...')
call(shlex.split(cmd_cleanup))
print('=> Done.')
