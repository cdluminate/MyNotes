class Solution:
    def mark_island(self, grid, mask, i, j) -> None:
        '''mark one island starting from i, j'''
        r, c = len(grid), len(grid[0])
        if i >= r or i < 0 or j >= c or j < 0:
            # case out of bound
            return None
        elif mask[i][j]:
            # case already explored
            return None
        elif '0' == grid[i][j] and not mask[i][j]:
            # case water, not explored
            mask[i][j] = True
            return None
        elif '1' == grid[i][j] and not mask[i][j]:
            # case land, not explored
            mask[i][j] = True
            self.mark_island(grid, mask, i, j+1)
            self.mark_island(grid, mask, i, j-1)
            self.mark_island(grid, mask, i+1, j)
            self.mark_island(grid, mask, i-1, j)
            return None
        else:
            raise Exception('this should not happen')


    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        count: int = 0
        r, c = len(grid), len(grid[0])
        explored = [[False for _ in range(c)] for _ in range(r)]
        for i in range(r):
            for j in range(c):
                value = grid[i][j]
                print('A', value, explored[i][j])
                if explored[i][j]:
                    # case explored
                    pass
                elif not explored[i][j] and '0' == value:
                    # case new water
                    explored[i][j] = True
                elif not explored[i][j] and '1' == value:
                    # case new island
                    self.mark_island(grid, explored, i, j)
                    count = count + 1
        assert all(all(x) for x in explored)
        return count
