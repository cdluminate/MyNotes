from collections import defaultdict
class Solution:
    def equalPairs(self, grid: List[List[int]]) -> int:
        r, c = len(grid), len(grid[0])
        # create row dict
        rowdict = defaultdict(int)
        for r in grid:
            vec = tuple(r)
            rowdict[vec] += 1
        # create column dict
        coldict = defaultdict(int)
        for i in range(c):
            vec = tuple(x[i] for x in grid)
            coldict[vec] += 1
        # count pairs
        result = 0
        for k in rowdict.keys():
            if k in coldict:
                result += rowdict[k] * coldict[k]
        return result
