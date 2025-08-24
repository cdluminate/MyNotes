class Solution:

    def buildGraph(self, equations: List[List[str]], values: List[float]) -> None:
        # mapping from (from, to) -> value
        self.graph: Dict[List[str],float] = dict()
        for ((x, y), z) in zip(equations, values):
            self.graph[(x, y)] = z # x/y = z
            self.graph[(y, x)] = 1/z # y/x = 1/z
        print('build graph>', self.graph)

    def inGraph(self, node: str) -> bool:
        return any([x[0] == node for x in self.graph.keys()])

    def findPath(self, qx: str, qy: str) -> float:
        # find a path from qx to qy, qx != qy
        def dfs(state: List[str]) -> List[str]:
            print('1state>', state)
            # find adjacent nodes
            prev = state[-1]
            adjacents = [x[1] for x in self.graph.keys() if x[0] == prev]
            adjacents = [x for x in adjacents if x not in state] # no loop
            print('2adjs>', adjacents)
            # if directly connected
            if qy in adjacents:
                return state + [qy]
            # not directly connected
            result = None
            for adj in adjacents:
                tmp = dfs(state + [adj])
                if tmp is not None:
                    result = tmp
                    break
            return result
        path = dfs([qx])
        print('find path>', qx, qy, path)
        return path

    def pathToValue(self, path: List[str]):
        # if no path
        if path is None:
            return -1.0
        # calculate the value
        accumulate = 1.0
        for i in range(len(path) - 1):
            value = self.graph[(path[i], path[i+1])]
            accumulate *= value
        print('path to value>', path, accumulate)
        return accumulate

    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        self.buildGraph(equations, values)
        result = []
        for (qx, qy) in queries:
            if qx == qy:
                result.append(1.0 if self.inGraph(qx) else -1.0)
                continue
            path = self.findPath(qx, qy)
            tmp = self.pathToValue(path)
            result.append(tmp)
        return result
