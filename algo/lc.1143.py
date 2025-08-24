class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        M, N = len(text1), len(text2)
        dp = [[None for _ in range(N)] for _ in range(M)]
        dp[0][0] = 1 if text1[0] == text2[0] else 0
        for i in range(M):
            for j in range(N):
                # skip initial state
                if dp[i][j] is not None: continue
                # dp[i,j] = max(dp[i-1][j], dp[i][j-1], 1(text1[i] == text2[j]) + dp[i-1][j-1])
                fromup = 0 if i-1 < 0 else dp[i-1][j]
                fromleft = 0 if j-1 < 0 else dp[i][j-1]
                this = 1 if text1[i] == text2[j] else 0
                diag = 0 if i-1<0 or j-1<0 else dp[i-1][j-1]
                dp[i][j] = max(fromup, fromleft, this+diag)
        return dp[-1][-1]

# XXX: timeout
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # reduce and conquer
        if not text1 or not text2:
            return 0
        elif text1[0] == text2[0]:
            return 1 + self.longestCommonSubsequence(text1[1:], text2[1:])
        else:
            drop1 = self.longestCommonSubsequence(text1[1:], text2)
            drop2 = self.longestCommonSubsequence(text1, text2[1:])
            return max(drop1, drop2)
