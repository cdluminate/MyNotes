class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        rows, cols = len(maze), len(maze[0])
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        initx, inity = entrance
        maze[initx][inity] = '+'
        q = [[initx, inity, 0]]

        while q:
            # fetch the current location
            x, y, level = q.pop(0)
            # traverse four directions
            for (dx, dy) in dirs:
                nx, ny = x + dx, y + dy
                # if it is not visited
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == '.':
                    # reach boundary?
                    if nx in (0, rows-1) or ny in (0, cols-1):
                        return level + 1
                    # not boundary
                    maze[nx][ny] = '+'
                    q.append([nx, ny, level+1])

        # when we finish without answer, there is no path
        return -1

class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:

        # validity test
        def is_valid(point: List[int]) -> bool:
            row, col = len(maze), len(maze[0])
            if point[0] < 0 or point[0] > row - 1:
                return False
            elif point[1] < 0 or point[1] > col - 1:
                return False
            else:
                return True

        # empty test
        def is_empty(point: List[int]) -> bool:
            return maze[point[0]][point[1]] == '.'
        
        # border test
        def is_border(point: List[int]) -> bool:
            row, col = len(maze), len(maze[0])
            if point[0] <= 0 or point[0] >= row - 1:
                return True
            elif point[1] <= 0 or point[1] >= col - 1:
                return True
            else:
                return False

        # find the path to exist
        def dfs(path: List[List[int]]) -> List[List[int]]:
            # XXX: path is always valid and empty
            # are we at boundary?
            src = path[-1]
            # try go four directions
            goup, godown, goleft, goright = None, None, None, None
            up = [src[0]-1, src[1]]
            if is_valid(up) and is_empty(up) and up not in path:
                if is_border(up):
                    return path + [up]
                goup = dfs(path + [up])
            down = [src[0]+1, src[1]]
            if is_valid(down) and is_empty(down) and down not in path:
                if is_border(down):
                    return path + [down]
                godown = dfs(path + [down])
            left = [src[0], src[1]-1]
            if is_valid(left) and is_empty(left) and left not in path:
                if is_border(left):
                    return path + [left]
                goleft = dfs(path + [left])
            right = [src[0], src[1]+1]
            if is_valid(right) and is_empty(right) and right not in path:
                if is_border(right):
                    return path + [right]
                goright = dfs(path + [right])
            # gather results
            results = [goup, godown, goleft, goright]
            results = [x for x in results if x is not None]
            # find the shortest path, or return None
            if not results:
                return None
            else:
                return min(results, key=lambda x: len(x))

        shortest_path = dfs([entrance])
        print('shortest path>', shortest_path)
        if shortest_path is None:
            return -1
        else:
            return len(shortest_path) - 1
