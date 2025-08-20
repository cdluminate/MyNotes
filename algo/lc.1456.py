class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        isvowel = lambda x: int(x in 'aeiouAEIOU')
        tmp = sum(map(isvowel, s[:k]))
        if len(s) <= k:
            return tmp
        maxsum = tmp
        for i in range(k, len(s)):
            to_pop = isvowel(s[i-k])
            to_add = isvowel(s[i])
            tmp = tmp - to_pop + to_add
            if tmp > maxsum:
                maxsum = tmp
        return maxsum
