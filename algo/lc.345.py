class Solution:
    def reverseVowels(self, s: str) -> str:
        vowels_val = []
        vowels_idx = []
        for i, x in enumerate(s):
            if x in 'aeiouAEIOU':
                vowels_val.append(x)
                vowels_idx.append(i)
        result = list(s)
        for i, x in zip(vowels_idx[::-1], vowels_val):
            result[i] = x
        return ''.join(result)

