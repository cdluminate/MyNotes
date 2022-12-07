class Solution:
    def hammingWeight(self, n: int) -> int:
        ret = 0
        for i in range(32):
            needle = (0b1 << i)
            if (n & needle) > 0:
                ret += 1
        return ret
