class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        longest = 0
        for i in range(len(s)):
            for j in range(i, len(s)+1):
                if len(s[i:j]) == len(set(s[i:j])):
                    if j - i > longest:
                        longest = j - i
                else:
                    break  # skip j
        return longest
