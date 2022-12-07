class Solution:
    def firstUniqChar(self, s: str) -> int:
        d = {}
        for char in s:
            if char in d:
                d[char] += 1
            else:
                d[char] = 1
        for (idx, char) in enumerate(s):
            if d[char] == 1:
                return idx
        return -1
