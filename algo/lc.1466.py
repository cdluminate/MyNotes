class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        # build adjacency list (to, from)
        adj: List[List[int]] = [[] for _ in range(n)]
        for con in connections:
            adj[con[0]].append([con[1], 1])
            adj[con[1]].append([con[0], 0])
        # dfs traverse
        self.count = 0
        def dfs(dest, prev):
            for (neighbor, direction) in adj[dest]:
                if neighbor != prev:
                    self.count += direction
                    dfs(neighbor, dest)
                else:
                    pass
        dfs(0, -1)
        return self.count

from collections import defaultdict

class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        # build undirected graph and roads
        graph = defaultdict(list)
        roads = list()
        for (i, j) in connections:
            graph[i].append(j)
            graph[j].append(i)
            roads.append((i, j))
        # traverse the graph with dfs
        self.changes = 0
        visited = [0]
        def dfs(dest):
            for neighbor in graph[dest]:
                # skip if already visited
                if neighbor in visited:
                    continue
                # do we need to revert the road
                if (neighbor, dest) not in roads:
                    self.changes += 1
                visited.append(neighbor)
                dfs(neighbor)
        dfs(0)
        return self.changes

class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        used = [False for _ in range(len(connections))]

        # number of reverts in the remaining conections to 
        def dfs(destination) -> int:
            # gather the list of adjacent nodes
            traverse = []
            for (i, c) in enumerate(connections):
                if used[i]: continue
                if destination in c:
                    traverse.append((i, c))
            # if used up
            if not traverse:
                return 0
            # mark the connections are used
            for (i, _) in traverse:
                used[i] = True
            # process connections
            tally = 0
            for (_, c) in traverse:
                if c[0] == destination:
                    tally += 1 + dfs(c[1])
                else:
                    tally += 0 + dfs(c[0])
            return tally
        
        return dfs(0)
