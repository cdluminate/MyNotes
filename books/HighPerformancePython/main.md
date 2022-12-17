High Performance Python
===
> Micha Gorelick, Ian Ozsvald, Oreilly.

supplemental material is available for download at https://github.com/mynameisfiber/high_performance_python

# chapter1: understanding performant python

pass

# chapter2: profiling to find bottlenecks

```
sudo apt install linux-perf
```

### begin with Julia set

This is a CPU-bound(计算密集型) problem.

See `juliaset.py`.

Simple approaches to timing -- print and a decorator.

Simple timing using the unix `/usr/bin/time` command. `/usr/bin/time --verbose command`

Using the cProfile module (the default profiler in python standard library).
```
python3 -m cProfile -s cumulative juliaset.py
and more
```

Using runsnakerun to Visualize cProfile output.

Using line_profiler for line-by-line measurements.

Using memory_profiler to diagnose memory usage.

Inspecting objects on the heap with heapy.

Using dowser for live graphing of instantiated variables.

Using the dis module.
```python
import dis

def fn_expressive(n = 1000):
  total = 0
  for i in range(n):
    total += i
  return total

def fn_terse(n = 1000):
  return sum(range(n))

dis.dis(fn_expressive)
dis.dis(fn_terse)
```

Unit testing during optimization to maintain correctness.

# chapter3: lists and tuples

lists are dynamic arrays while tuples are static arrays.

list lookup runs in O(1), while list.index() runs in O(n) by performing linear search.

# chapter4: dictionaries and sets

pass

# chapter5: iterators and genetators

pass

# chapter6: matrix and vector computation

TODO

# chapter7: Compiling to C

* Cython -- (most commonly used) mixture of C and python  
* Shed -- Python2C converter  
* Numba -- LLVM-based  
* PyPy -- JIT  

* FFI  

TODO

# chapter8: Concurrency

async

# chapter9: The multiprocessing Module

TODO

# chapter10: Cluster and Job Queues

TODO

# chapter11: Using Less RAM

TODO

Tips:  
1. Use numpy if you are working with numeric data.  

# chapter12: Lessons from the Field

TODO

Nice book.
