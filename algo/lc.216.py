class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        # DFS for all combinations
        results = []
        def dfs(path) -> None:
            # stop criterion
            if len(path) == k:
                # only record the path if sums to n
                if sum(path) == n:
                    results.append(path)
            else:
                # find numbers to traverse
                to_traverse = [x for x in range(1,9+1) if x not in path]
                for i in to_traverse:
                    dfs(path + [i])
        dfs([])
        # deduplicate
        results = [set(x) for x in results]
        new_results = []
        for i in results:
            if i not in new_results:
                new_results.append(i)
        new_results = [list(x) for x in new_results]
        return new_results
