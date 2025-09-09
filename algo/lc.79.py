from typing import *
import itertools as it

board = [['A','B','C','E'],
         ['S','F','C','S'],
         ['A','D','E','E']]
word = 'ABCCED'

def dfs(board: List[List[str]],
        state: str,
        trajectory: List[Tuple[int]]) -> bool:
    print('call>', state, trajectory)
    m = len(board)
    n = len(board[0])
    #print('m, n', m, n)
    if not state:
        return True
    else:
        # if can go up
        results = []
        directions = [(-1, 0), (+1, 0), (0, +1), (0, -1)]
        for direction in directions:
            prev = trajectory[-1]
            newi, newj = prev[0] + direction[0], prev[1] + direction[1]
            #print('traj', trajectory, newi, newj)
            # boundary
            if newi < 0 or newi >= m:
                continue
            if newj < 0 or newj >= n:
                continue
            # try
            charmatch = board[newi][newj] == state[0]
            #print('match?', board[newi][newj], state[0], charmatch)
            isloop = (newi, newj) in trajectory
            new_traj = trajectory + [(newi, newj)]
            if charmatch and not isloop:
                #print('next-dfs', charmatch, isloop)
                tmp = dfs(board, state[1:], new_traj)
                results.append(tmp)
            else:
                results.append(False)
        # any direction valid?
        #print('debug>', state, trajectory, any(results))
        return any(results)

if __name__ == '__main__':
    m, n = len(board), len(board[0])
    # find the heads
    matches = []
    for (i, j) in it.product(range(m), range(n)):
        if board[i][j] == word[0]:
            matches.append((i, j))
    #print('matches>', matches)
    # dfs on each head
    found = False
    for head in matches:
        #print('head>', head)
        result = dfs(board, word[1:], [head])
        if result:
            found = True
    print('result:', found)
    
