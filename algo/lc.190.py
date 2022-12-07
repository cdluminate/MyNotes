class Solution:
    def reverseBits(self, n: int) -> int:
        new = 0
        for i in range(32):
            needle = 0b1 << i
            flag = (n & needle) > 0
            if flag:
                insert = (0b1 << 31) >> i
                new = new | insert
        return new
