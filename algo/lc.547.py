class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        N = len(isConnected)
        visited = [False for _ in range(N)]
        provinces = 0

        def dfs(city: int):
            # mark it as visited
            visited[city] = True
            for neighbor in range(N):
                if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                    dfs(neighbor)

        for i in range(N):
            if not visited[i]:
                dfs(i)
                provinces += 1

        return provinces

class Solution:

    def findCircle(self, isConnected, visited):
        if all(visited):
            return []
        # find the first unvisited city
        idx = visited.index(False)
        province = [idx]
        visited[idx] = True
        N = len(isConnected)
        # explore first province using bfs
        to_traverse = [i for i in range(N) if not visited[i] and isConnected[idx][i]]
        while to_traverse:
            new_traverse = []
            for city in to_traverse:
                # add new city and mark as visited
                province.append(city)
                visited[city] = True
                # collect all unvisited new cities
                new_traverse.extend([i for i in range(N) if not visited[i] and isConnected[city][i]])
            # update bfs queue
            to_traverse = new_traverse
        return province

    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        provinces: List[List[int]] = []
        visited: List[bool] = [False for _ in range(len(isConnected))]
        while not all(visited):
            new_province = self.findCircle(isConnected, visited)
            print('new province >>', new_province)
            if new_province:
                provinces.append(new_province)
        return len(provinces)


