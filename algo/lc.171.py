class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        res = 0
        for (i, char) in enumerate(reversed(columnTitle)):
            res += (ord(char) - ord('A') + 1) * (26 ** i)
        return res
