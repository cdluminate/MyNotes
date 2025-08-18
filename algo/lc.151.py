class Solution:
    def reverseWords(self, s: str) -> str:
        tokens = s.split()
        return ' '.join(tokens[::-1])
