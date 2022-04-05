#!/usr/bin/python3
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


def cbdump(v: list) -> str:
    '''
    Construct a textural representation of the checkboard.
    '''
    n = len(v)
    rows = [['Q ' if v[i]==j else '. ' for j in range(n)] for i in range(n)]
    rows = '\n'.join([''.join(row) for row in rows])
    return rows


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

if __name__ == '__main__':
    test_validate()
