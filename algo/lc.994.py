class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        # is it valid grid?
        if not grid:
            return 0
        rows, cols = len(grid), len(grid[0])

        # find the initial rotten ones
        seeds = []
        levels = []
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 2:
                    seeds.append([i, j])
                    levels.append([i, j, 0])

        # do BFS and pollute all oranges
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for seed in seeds:
            # pollute all connected from this seed
            traverse = [seed + [0]]
            while traverse:
                x, y, level = traverse.pop(0)
                # go four directions
                for (dx, dy) in directions:
                    nx, ny = x + dx, y + dy
                    # is it orange 1?
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1:
                        grid[nx][ny] = 2
                        levels.append([nx, ny, level+1])
                        traverse.append([nx, ny, level+1])
                    # is it orange 2 but higher level?
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 2:
                        cursor = 0
                        while levels[cursor][:2] != [nx, ny]:
                            cursor += 1
                        if levels[cursor][-1] > level + 1:
                            levels[cursor][-1] = level + 1
                            traverse.append([nx, ny, level+1])

        # is there any good orange?
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    return -1

        # is there orange at all?
        if sum([sum(r) for r in grid]) == 0:
            return 0

        # find the maximum level
        maxlevel = max(levels, key=lambda x: x[-1])
        return maxlevel[-1]


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        # is it valid grid?
        if not grid:
            return 0
        rows, cols = len(grid), len(grid[0])

        # find the initial rotten ones
        seeds = []
        levels = []
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 2:
                    seeds.append([i, j])
                    levels.append([i, j, 0])

        # do BFS and pollute all oranges
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for seed in seeds:
            # pollute all connected from this seed
            traverse = [seed + [0]]
            while traverse:
                x, y, level = traverse.pop(0)
                # go four directions
                for (dx, dy) in directions:
                    nx, ny = x + dx, y + dy
                    # is it orange 1?
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1:
                        traverse.append([nx, ny, level+1])
                        levels.append([nx, ny, level+1])
                        grid[nx][ny] = 2

        # is there any good orange?
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    return -1

        # is there orange at all?
        if sum([sum(r) for r in grid]) == 0:
            return 0

        # find the maximum level
        maxlevel = max(levels, key=lambda x: x[-1])
        return maxlevel[-1]
