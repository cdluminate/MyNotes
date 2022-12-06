class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        d = dict()
        for char in magazine:
            if char not in d:
                d[char] = 1
            else:
                d[char] = d[char] + 1
        for char in ransomNote:
            if char not in d:
                return False
            else:
                d[char] = d[char] - 1
                if d[char] <= 0:
                    d.pop(char)
        return True
