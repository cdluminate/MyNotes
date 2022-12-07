class Solution:
    def isAlphaNumeric(self, c: str):
        # len(c) must be 1
        return c.isalpha() or c.isdigit()
    def isPalindrome(self, s: str) -> bool:
        newstr = [x for x in s.lower() if self.isAlphaNumeric(x)]
        return newstr == newstr[::-1]
