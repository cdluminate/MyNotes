import numpy as np
import rich
from rich.progress import track
c = rich.get_console()

def validate(rep: np.ndarray) -> bool:
    '''
    Validate the given solution. Both vector and square
    matrix representations are acceptable.
    '''
    if len(rep.shape) == 1:
        rep2 = np.zeros((len(rep), len(rep)))
        rep2[np.arange(len(rep)), rep] = 1
    elif len(rep.shape) == 2:
        rep2 = rep
    else:
        raise ValueError('invalid shape for solution')
    N = rep2.shape[0]
    # check1: row conflict
    if not all(rep2.sum(axis=1) <= 1):
        return False
    # check2: column conflict
    if not all(rep2.sum(axis=0) <= 1):
        return False
    # check3: diagonals conflict
    if not all(rep2.diagonal(i).sum() <=1
            for i in range(-(N-1),N)):
        return False
    # check4: opposite diagonals conflict
    if not all(rep2[::-1,:].diagonal(i).sum() <=1 for i in range(-(N-1),N)):
        return False
    return True


def test_validate():
    sol = np.array([5,3,1,7,2,8,6,4]) - 1
    assert(validate(sol))

if __name__ == '__main__':
    test_validate()
