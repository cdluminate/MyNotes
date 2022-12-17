#!/bin/sh
set -e
# Effective Python: 59 specific ways to write better python

# helper stuff
PY=/usr/bin/python3

## Pythonic thinking
$PY -c "import this;"

#1. know your python version: sys.version_info

#2. follow pep8

#3. str, bytes, unicode

#4. helper functions instead of complex expressions

#5. slicing

#6. avoid using start, end, and stride in a single slice

#7. use list comprehensions instead of map and filter

#8. avoid more than two expressions in list comprehensions

#9. consider generator expressions for large comprehensions

#10. prefer enumerate over range

#11. use zip to process iterators in parallel

#12. avoid else blocks after for and while loops

#13. take advantage of each block in try/except/else/finally

## Functions

#14. prefer exceptions to returning None

#15. know how closures interact with variable scope | TODO

#16. consider generators instead of returning lists | TODO

#17. be defensive when iterting over arguments | pass

#18. reduce visual noise with variable positional arguments | pass

#19. provide optional behaviour with keyword arguments | pass

#20. use None and Docstrings to specify dynamic default arguments

#21. enforce clarity with keyword-only arguments

## Classes and inheritance

#22. prefer helper classes over bookkeeping with dictionaries and tuples

#23. accept functions for simple interfaces instead of classes

#24. use @classmethod pylomorphism to construct objects generically | pass

#25. initialize parent classes with super

#26. use multiple inheritance only for mex-in utility classes | pass

#27. prefer public attributes over private ones

#28. inherit from collections.abc for custom container types

## Metaclasses and attributes

#29. use plain attributes instead of get and set methods

#30. consider @property instead of refactoring attributes

#31. use descriptors for reusable @property methods | pass

#32. use __getattr__, __getattribute__, and __setattr__ for lazy attributes

#33. validate subclasses with metaclasses | pass

#34. register class existence with metaclasses | pass

#35. annotate class attributes with metaclasses | pass

## Concurrency and parallelism

#36. use subprocess to manage child processes

#37. use Threads for blocking I/O, avoid for parallelism | pass

#38. use Lock to prevent data races in threads

#39. use queue to coordinate work between threads

#40. consider coroutines to run many functions concurrently

#41. consider concurrent.futures for true parallelism | pass

## Built-in modules

#42. define function decorators with functools.wraps | TODO

#43. consider contextlib and with statements for reusable try/finally behavior

#44. make pickle reliable with copyreg | pass

#45. use datetime instead of time for local clocks

#46. use built-in algorithms and data structures

#47. use decimal when precision is paramount

#48. know where to find community-built modules | pass

## Collaboration

#49. write docstrings for every function, class, and module

#50. use packages to organize modules and provide stable APIs

#51. define a root exception to insulate callers from APIs

#52. know how to break circular dependencies

#53. use virtual environments for isolated and reproducible dependencies

## Production

#54. consider module-scoped code to configure deployment environments

#55. use repr strings for debugging output

#56. test everything with unittest

#57. consider interactive debugging with pdb

#58. profile before optimizing

#59. use tracemalloc to understand memory usage and leaks

#EOF
