import itertools as it
class Solution:
    def dfs(self, board: List[List[str]], state: str, traj: List[Tuple[int]]):
        if not state:
            # consumed all characters
            return True
        else:
            # explore every direction
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            results = []
            for d in directions:
                prev = traj[-1]
                curr = (prev[0] + d[0], prev[1] + d[1])
                # boundary check
                if curr[0] < 0 or curr[0] >= len(board):
                    continue
                if curr[1] < 0 or curr[1] >= len(board[0]):
                    continue
                # character match
                charmatch = board[curr[0]][curr[1]] == state[0]
                # is it a loop?
                isloop = curr in traj
                # result for this direction
                if charmatch and not isloop:
                    tmp = self.dfs(board, state[1:], traj + [curr])
                    results.append(tmp)
                else:
                    results.append(False)
            return any(results)
    def exist(self, board: List[List[str]], word: str) -> bool:
        if not board:
            return False
        if not word:
            return True
        # find the starting points
        matches = []
        for (i, j) in it.product(range(len(board)), range(len(board[0]))):
            if board[i][j] == word[0]:
                matches.append((i, j))
        # if not matches
        if not matches:
            return False
        else:
            for m in matches:
                if self.dfs(board, word[1:], [m]):
                    return True
            return False
        
