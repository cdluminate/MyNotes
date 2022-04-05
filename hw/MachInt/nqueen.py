#!/usr/bin/pypy3
import time
import rich
from collections import Counter
from rich.progress import track
c = rich.get_console()

def isvalid(v: list, n: int = None, debug: bool = False) -> bool:
    '''
    Tells whether the given vector `v` is a valid solution for n-queen.
    The vector is a row-based representation of the checkboard.
    v[0] == 0 means the queen for the first row is placed at the first column.
    '''
    # dealing with convenience call
    if v and (n is None):
        n = len(v)
    # helper function for checking diagonal attack
    def _diag_attack(_v: list, debug: bool = False):
        c = Counter(i - _v[i] for i in range(len(_v)))
        return any(count > 1 for count in c.values())
    # check1: completeness
    if len(v) < n:
        if debug:
            print('Reason: incomplete', len(v), n)
        return False
    # check2: column attack
    # note, row representation is free from row attack
    if not all(x <= 1 for x in Counter(v).values()):
        if debug:
            print('Reason: column attack', Counter(v))
        return False
    # check3: diagonal attack
    if _diag_attack(v, debug) or _diag_attack(list(reversed(v)), debug):
        if debug:
            print('Reason: diagonal attack')
        return False
    # passed all checks
    return True


def test_validate():
    sol = [x-1 for x in [5,3,1,7,2,8,6,4]]
    c.print(cbdump(sol))
    assert(isvalid(sol, debug=True))
    sol = [x-1 for x in [1,1,1,1,1,1,1,1]]
    c.print(cbdump(sol))
    assert(not isvalid(sol, debug=True))
    sol = [x-1 for x in [1,2,3,4,5,6,7,8]]
    c.print(cbdump(sol))
    assert(not isvalid(sol, debug=True))


def cbdump(v: list) -> str:
    '''
    Construct a textural representation of the checkboard.
    '''
    n = len(v)
    rows = [['Q ' if v[i]==j else '. ' for j in range(n)] for i in range(n)]
    rows = '\n'.join([''.join(row) for row in rows])
    return rows


def solve_nqueen_dfs(n: int):
    '''
    Naive n-queen solver in dfs, brute-force permutation method.
    '''
    def _solve_nqueen_dfs(v: list, n: int):
        '''
        recursive worker function for solve_nqueen_dfs.
        validate solution when reached the leaf node
        '''
        cursor = len(v)
        # recursion boundary
        if cursor == n:
            if isvalid(v):
                return v
            else:
                return False
        else:
            for i in range(n):
                v.append(i)
                ret = _solve_nqueen_dfs(v, n)
                if ret:
                    return ret
                else:
                    v.pop()
    return _solve_nqueen_dfs([], n)


def benchmark_nqueen(n: int):
    '''
    benchmark differnt solvers and make plot
    '''
    solvers = [solve_nqueen_dfs]
    elapsed = []
    for solver in solvers:
        tm_start = time.time()
        sol = solver(n)
        tm_end = time.time()
        elapsed.append(tm_end - tm_start)
    print('Elapsed time:')
    for i in range(len(solvers)):
        print(f'[{i}]', solvers[i].__name__, elapsed[i])


if __name__ == '__main__':
    #test_validate()
    #v = solve_nqueen_dfs(8)
    #c.print(cbdump(v))
    benchmark_nqueen(8)
