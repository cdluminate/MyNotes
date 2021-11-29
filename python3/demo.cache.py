#!/usr/bin/python3
from time import sleep
from functools import lru_cache

# __

@lru_cache(None)
def add(x: int, y: int) -> int:
    print(' * add', x, y)
    return x + y

print(add(1, 2))
print(add(3, 4))
print(add(1, 2))

# __

def fac_nocache(n: int) -> int:
    print(' * nocache, n=', n)
    sleep(0.1)
    return 1 if n <= 1 else n*fac_nocache(n-1)

@lru_cache(None)
def fac_cached(n: int) -> int:
    print(' * cached, n=', n)
    sleep(0.1)
    return 1 if n <= 1 else n*fac_cached(n-1)

a, b = fac_nocache(16), fac_cached(16)
print(a, b)
c, d = fac_nocache(16), fac_cached(16)
print(c, d)
e = fac_cached(16)
print(e)
