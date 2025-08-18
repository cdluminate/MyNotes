class Solution:
    def dfs(self, grid, i: int, j: int):
        r, c = len(grid), len(grid[0])
        if i < 0 or i >= r or j < 0 or j >= c:
            # case out of bound
            return
        elif grid[i][j] == '0':
            # case water
            return
        elif grid[i][j] == '1':
            # case land
            grid[i][j] = '0' # mark it as explored
            self.dfs(grid, i-1, j)
            self.dfs(grid, i+1, j)
            self.dfs(grid, i, j-1)
            self.dfs(grid, i, j+1)
        else:
            raise Exception('this should not happen')
        

    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        count = 0
        r, c = len(grid), len(grid[0])
        for i in range(r):
            for j in range(c):
                # if land, mark a new island
                if grid[i][j] == '1':
                    count += 1
                    self.dfs(grid, i, j)
        return count
