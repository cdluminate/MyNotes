class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[None for _ in range(n)] for _ in range(m)]
        dp[0][0] = 1
        for i in range(m):
            for j in range(n):
                # skip the init point
                if dp[i][j] is not None:
                    continue
                # dp[i][j] = dp[i-1][j] + dp[i][j-1]
                fromup = 0 if i-1 < 0 else dp[i-1][j]
                fromleft = 0 if j-1 < 0 else dp[i][j-1]
                dp[i][j] = fromup + fromleft
        return dp[-1][-1]
