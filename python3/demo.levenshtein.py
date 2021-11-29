from typing import *
import numpy as np
import unittest
import numba
import sys
import time


@numba.jit
def LevenshteinCostly(u: Any, v: Any) -> float:
    '''
    Calculate the Levenshtein distance between two strings.
    :cite: https://en.wikipedia.org/wiki/Levenshtein_distance
    '''
    if max(len(u), len(v)) == 0:
        return 0.;
    dp = np.zeros((len(u)+1, len(v)+1), dtype=np.int)
    dp[:, 0] = np.arange(len(u)+1)
    dp[0, :] = np.arange(len(v)+1)
    for i in range(1, len(u)+1):
        for j in range(1, len(v)+1):
            if u[i-1] == v[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                replace = dp[i-1][j-1] + 1
                iinsert = dp[i-1][j] + 1
                jinsert = dp[i][j-1] + 1
                dp[i][j] = min(replace, iinsert, jinsert)
    return dp[dp.shape[0]-1][dp.shape[1]-1]


@numba.jit
def Levenshtein(u: Any, v: Any) -> float:
    '''
    Calculate the Levenshtein distance between two strings.
    :cite: https://en.wikipedia.org/wiki/Levenshtein_distance
    '''
    if max(len(u), len(v)) == 0:
        return 0
    elif min(len(u), len(v)) == 0:
        return max(len(u), len(v))
    elif u[0] == v[0]:
        return Levenshtein(u[1:], v[1:])
    else:
        replace = Levenshtein(u[1:], v[1:]) + 1
        iinsert = Levenshtein(u[1:], v) + 1
        jinsert = Levenshtein(u, v[1:]) + 1
        return min(replace, iinsert, jinsert)


class TestLevenshtein(unittest.TestCase):
    def test_ident(self):
        d = LevenshteinCostly('abc', 'abc')
        self.assertTrue(abs(d - 0) < 1e-7, d)
        d = Levenshtein('abc', 'abc')
        self.assertTrue(abs(d - 0) < 1e-7, d)
    def test_diff(self):
        d = LevenshteinCostly('abc', 'cba')
        self.assertTrue(abs(d - 2) < 1e-7, d)
        d = Levenshtein('abc', 'cba')
        self.assertTrue(abs(d - 2) < 1e-7, d)
    def test_empty(self):
        d = LevenshteinCostly('', '')
        self.assertTrue(abs(d - 0) < 1e-7, d)
        d = Levenshtein('', '')
        self.assertTrue(abs(d - 0) < 1e-7, d)
    def test_list(self):
        d = Levenshtein([1,2,3], [2,3,1])
        self.assertTrue(abs(d - 2) < 1e-7, d)
        d = LevenshteinCostly([1,2,3], [2,3,1])
        self.assertTrue(abs(d - 2) < 1e-7, d)
    def test_array_ident(self):
        x = list(np.arange(10))
        d = LevenshteinCostly(x, x)
        self.assertTrue(abs(d - 0) < 1e-7, d)
    def test_array_diff(self):
        x = list(np.arange(10))
        d = LevenshteinCostly(x, x[::-1])
        self.assertTrue(abs(d - 10) < 1e-7, d)
    def test_ground_truth(self):
        d = Levenshtein('saturday', 'sunday')
        self.assertTrue(d == 3, d)
        d = LevenshteinCostly('saturday', 'sunday')
        self.assertTrue(d == 3, d)
    def test_ground_truth2(self):
        d = Levenshtein('sitting', 'kitten')
        self.assertTrue(d == 3)
        d = Levenshtein('sitting', 'kitten')
        self.assertTrue(d == 3)



if __name__ == '__main__':
    sys.setrecursionlimit(65536)
    N = 100
    x = np.argsort(np.random.random(N)).flatten()
    y = np.argsort(np.random.random(N)).flatten()
    print(x, y)

    #t = time.time()
    #d = Levenshtein(x, y)
    #print(time.time() - t, d)

    t = time.time()
    d = LevenshteinCostly(x, y)
    print(time.time() - t, d)

    for N in range(1, 300):
        x = np.arange(N)
        y = x[::-1].ravel()
        d = LevenshteinCostly(x, y)
        print(N, '->', d)
