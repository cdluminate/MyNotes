#!/usr/bin/python3
'''
doctest demo
ref: https://docs.python.org/3.5/library/doctest.html
'''

def factorial(n:int):
    '''Return the factorial of integer n, n>=0

    >>> [factorial(n) for n in range(6)]
    [1, 1, 2, 6, 24, 120]

    >>> factorial(30)
    265252859812191058636308480000000

    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: n:int must be >= 0

    >>> factorial(30.1)
    Traceback (most recent call last):
        ...
    ValueError: n must be int
    '''
    if not n>=0: raise ValueError("n:int must be >= 0")
    if not isinstance(n, int): raise ValueError("n must be int")
    #if n+1==n: raise OverflowError("n too large") # n=1e300
    return 1 if n<=1 else n*factorial(n-1)

if __name__=='__main__':
    import doctest
    doctest.testmod()

'''
python3 demo.doctest.py -v
'''
