#!/usr/bin/pypy3
import time
import itertools as it
import functools as ft
import random
import math
import rich
from collections import Counter
from rich.progress import track
c = rich.get_console()
random.seed(1)


def cbdump(v: list) -> str:
    '''
    Construct a textural representation of the checkboard.
    '''
    n = len(v)
    rows = [['Q ' if v[i]==j else '. ' for j in range(n)] for i in range(n)]
    rows = '\n'.join([''.join(row) for row in rows])
    return rows


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


def test_isvalid():
    sol = [x-1 for x in [5,3,1,7,2,8,6,4]]
    #c.print(cbdump(sol))
    assert(isvalid(sol, debug=True))
    sol = [x-1 for x in [1,1,1,1,1,1,1,1]]
    #c.print(cbdump(sol))
    assert(not isvalid(sol, debug=True))
    sol = [x-1 for x in [1,2,3,4,5,6,7,8]]
    #c.print(cbdump(sol))
    assert(not isvalid(sol, debug=True))
    return True


def solve_nqueen_dfs(n: int):
    '''
    Naive n-queen solver in dfs, brute-force permutation method.
    '''
    def _solve_nqueen_dfs(v: list, n: int):
        '''
        recursive worker function
        '''
        cursor = len(v)
        # recursion boundary: validate solution
        if cursor == n:
            if isvalid(v):
                return v
            else:
                return False
        # not yet reached at leaf node
        else:
            for i in range(n):
                v.append(i)
                ret = _solve_nqueen_dfs(v, n)
                if ret:
                    return ret
                else:
                    v.pop()
    return _solve_nqueen_dfs([], n)


def solve_nqueen_backtrack(n: int):
    '''
    backtrack depth-first search for n-queen
    '''
    def _solve_nqueen_backtrack(v: list, n: int):
        '''
        recursive worker function
        '''
        cursor = len(v)
        # recursion boundary: validate solution
        if cursor == n:
            if isvalid(v):
                return v
            else:
                return False
        # not yet reached at leaf node
        else:
            for i in range(n):
                v.append(i)
                if not isvalid(v):
                    # prune the search sub tree
                    v.pop()
                else:
                    ret = _solve_nqueen_backtrack(v, n)
                    if ret:
                        return ret
                    else:
                        v.pop()
    return _solve_nqueen_backtrack([], n)


def attack_score(v: list) -> int:
    '''
    Gives an attack score for the complete or partial solution v.
    This function is a variant to the previous `isvalid(...)` function.
    When attack_score(...) reached at 0, the given solution is valid.
    '''
    attacks = 0
    # helper function for counting diagonal attack
    def _diag_attack(_v: list) -> int:
        c = Counter(i - _v[i] for i in range(len(_v)))
        return sum(max(count-1,0) for count in c.values())
    # type1: column attack
    attacks += sum(max(x-1, 0) for x in Counter(v).values())
    # type2: diagonal attack
    attacks += _diag_attack(v)
    attacks += _diag_attack(list(reversed(v)))
    return attacks


def test_attack_score():
    sol = [x-1 for x in [5,3,1,7,2,8,6,4]]
    assert(attack_score(sol) == 0)
    sol = [x-1 for x in [1,1,1,1,1,1,1,1]]
    assert(attack_score(sol) == 7)
    sol = [x-1 for x in [1,2,3,4,5,6,7,8]]
    assert(attack_score(sol) == 7)
    return True


def solve_nqueen_hill(n: int, numretry: int = 10):
    '''
    Hill-climbing (steepest) search / Greedy local search.
    We want to minimize attack_score starting from a random guess.
    '''
    def _solve_nqueen_hill(v: list, n: int, debug: bool = False):
        def _action_score(v: list, act: tuple) -> int:
            '''
            evaluate the score after performing the action
            '''
            tmp = v.copy()
            tmp[act[0]], tmp[act[1]] = tmp[act[1]], tmp[act[0]]
            return attack_score(tmp)
        for iteration in range(n):
            # evaluate the current attack_score
            current_score = attack_score(v)
            if debug:
                print('iter', iteration, 'currernt score', current_score)
            # evaluate 
            action_scores = [(action, _action_score(v, action))
                    for action in it.combinations(range(n), 2)]
            action_scores.sort(key=lambda x: x[1])  # smallest goes to top
            if debug:
                print(action_scores)
            # is there any better solution?
            if action_scores[0][1] < current_score:
                # take the action
                act = action_scores[0][0]
                v[act[0]], v[act[1]] = v[act[1]], v[act[0]]
                print('swapped', act, 'and the result is', v)
                current_score = action_scores[0][1]
            else:
                break
        return v, current_score
    # initliaze with a random guess
    # we use a fixed random seed to ensure reproducibility
    for itry in range(numretry):
        v = list(range(n))
        random.shuffle(v)
        print('trial', itry, 'starts with', v)
        sol, score = _solve_nqueen_hill(v, n, False)
        if score > 0:
            print('trial', itry, 'stuck in local minima')
        else:
            return v
    return None


def solve_nqueen_simanneal(n: int, numretry: int = 10):
    '''
    Simulated Annealing, another local search method.
    '''
    def _solve_nqueen_simanneal(v: list, n: int, maxiter: int = 1000,
            debug: bool = False):
        def _action_score(v: list, act: tuple) -> int:
            '''
            evaluate the score after performing the action
            '''
            tmp = v.copy()
            tmp[act[0]], tmp[act[1]] = tmp[act[1]], tmp[act[0]]
            return attack_score(tmp)
        for iteration in range(maxiter):
            # evaluate the current attack_score
            current_score = attack_score(v)
            if debug:
                print('iter', iteration, 'currernt score', current_score)
            # evaluate 
            act = random.choice(list(it.combinations(range(n), 2)))
            score = _action_score(v, act)
            # is there any better solution?
            if score < current_score:
                # take the action
                v[act[0]], v[act[1]] = v[act[1]], v[act[0]]
                if debug:
                    print('swapped', act, 'and the result is', v)
                current_score = score
            else:
                # stuck at local minima, we try to jump out
                threshold = iteration / maxiter
                if random.random() >= threshold:
                    v[act[0]], v[act[1]] = v[act[1]], v[act[0]]
                    if debug:
                        print('annealing', act, 'and the result is', v)
        return v, current_score
    # initliaze with a random guess
    # we use a fixed random seed to ensure reproducibility
    for itry in range(numretry):
        v = list(range(n))
        random.shuffle(v)
        print('trial', itry, 'starts with', v)
        sol, score = _solve_nqueen_simanneal(v, n, 1000, False)
        if score > 0:
            print('trial', itry, 'stuck in local minima')
        else:
            return v
    return None


def solve_nqueen_beam(n: int, numretry: int = 10, sbeam: int = 5):
    '''
    Greedy local beam search. It is not k-start hill climbing.
    sbeam is size of beam. default to 3.
    '''
    def _solve_nqueen_beam(beam: list, n: int, debug: bool = False):
        '''
        beam is a list of solutions.
        '''
        def _take_action(v: list, act: tuple) -> int:
            tmp = v.copy()
            tmp[act[0]], tmp[act[1]] = tmp[act[1]], tmp[act[0]]
            return tmp, attack_score(tmp)
        for iteration in range(n):
            # evaluate the current attack_score
            current_score = min(attack_score(v) for v in beam)
            if debug:
                print('iter', iteration, 'currernt score', current_score)
            # evaluate steepest step for every item in beam
            candidates = []
            for v in beam:
                candidates.extend([_take_action(v, action)
                    for action in it.combinations(range(n), 2)])
            candidates.sort(key=lambda x: x[1])  # smallest goes to top
            if debug:
                print(candidates[:sbeam])
            # is there any better solution?
            if candidates[0][1] < current_score:
                # take the action
                beam = [x[0] for x in candidates[:sbeam]]
                current_score = candidates[0][1]
            else:
                break
        return beam, current_score
    # initliaze with a random guess
    # we use a fixed random seed to ensure reproducibility
    for itry in range(numretry):
        beam = [list(range(n)) for _ in range(sbeam)]
        for i in range(sbeam):
            random.shuffle(beam[i])
        print('trial', itry, 'starts with', beam)
        sol, score = _solve_nqueen_beam(beam, n, True)
        if score > 0:
            print('trial', itry, 'stuck in local minima')
        else:
            return sol[0]
    return None


def benchmark_nqueen(n: int):
    '''
    benchmark differnt solvers and make plot
    '''
    solvers = [
            solve_nqueen_dfs,
            solve_nqueen_backtrack,
            solve_nqueen_hill,
            solve_nqueen_simanneal,
            solve_nqueen_beam,
            ]
    elapsed = []
    print('Elapsed time:')
    for (i, solver) in enumerate(solvers):
        tm_start = time.time()
        sol = solver(n)
        tm_end = time.time()
        print(cbdump(sol))
        elapsed.append(tm_end - tm_start)
        print(f'[{i}]', solvers[i].__name__, elapsed[i])
    import matplotlib.pyplot as plt
    plt.bar([x.__name__ for x in solvers], [math.log(1000*x) for x in elapsed])
    plt.xticks(rotation=30)
    plt.show()


if __name__ == '__main__':
    #test_isvalid()
    #test_attack_score()
    #v = solve_nqueen_dfs(8)
    #v = solve_nqueen_backtrack(8)
    #v = solve_nqueen_hill(8)
    #v = solve_nqueen_simanneal(8)
    #v = solve_nqueen_beam(8)
    #c.print(cbdump(v))
    #print(isvalid(v), attack_score(v))
    benchmark_nqueen(8)
