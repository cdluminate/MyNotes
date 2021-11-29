#!/usr/bin/python3
'''
implementation of some basic algorithms.

TODO: use unittest or doctest instead of the __main__ part
'''
from typing import *

def bisearch(nums: List[int], needle: int) -> bool:
    ''' the input list ``nums`` must be sorted (ascending) first.
    Complexity: O(log_2 N)
    '''
    if not nums:
        return False
    curl, curr = 0, len(nums)-1 # NOTE: don't drop -1
    while curl <= curr:
        curm = int( (curl+curr)/2 )
        if nums[curm] == needle:
            return True
        elif nums[curm] > needle:
            curr = curm-1 # NOTE: don't drop -1
        else: # nums[curm] < needle
            curl = curm+1 # NOTE: don't drop +1
        #print(curl, curr)
    return False

def qsort(v: List[int]) -> List[int]:
    ''' quick sort algorithm, one-liner. non-inplace
    '''
    return v if len(v)==0 else \
            (qsort([x for x in v[1:] if x>=v[0]]) + \
            [v[0]] + \
            qsort([x for x in v[1:] if x<v[0]]))


if __name__=='__main__':
    a = [1, 2, 3, 6, 2, 1, 2, 45, 7, 4, 9, 50]
    a.sort() # ascending

    print(bisearch(a, 45))
    print(bisearch(a, 44))
    print(bisearch(a, -1))
    print(bisearch([], 42))

    a = list(map(int,'4 8 7 5 3 3 7 9 6 4 8 1'.split()))
    print(a)
    print(qsort(a))
