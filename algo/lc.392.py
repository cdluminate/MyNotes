class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        cursor_s = 0
        cursor_t = 0
        while cursor_s < len(s) and cursor_t < len(t):
            if s[cursor_s] == t[cursor_t]:
                cursor_s += 1
                cursor_t += 1
            else:
                cursor_t += 1
        return cursor_s == len(s)
