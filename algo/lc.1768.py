class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        # Create a list to store characters, which is much more efficient
        result_list = []

        # Get the lengths of both words
        len1, len2 = len(word1), len(word2)
        min_len = min(len1, len2)

        # 1. Loop through the common part
        for i in range(min_len):
            result_list.append(word1[i])
            result_list.append(word2[i])

        # 2. Append the remaining "tail" from the longer word
        # Slicing will correctly handle which word is longer.
        # If word1 is longer, word1[min_len:] gets the rest.
        # If word2 is longer, word2[min_len:] gets the rest.
        result_list.append(word1[min_len:])
        result_list.append(word2[min_len:])

        # 3. Join the list into a single string - very fast! ✅
        return "".join(result_list)

class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        len1 = len(word1)
        len2 = len(word2)
        maxlen = max(len1, len2)
        result = ''
        for i in range(maxlen):
            if i < len1:
                result += word1[i]
            if i < len2:
                result += word2[i]
        return result

class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        minlen = min(len(word1), len(word2))
        result = []
        for (x, y) in zip(word1, word2):
            result.extend([x, y])
        rest = word1[minlen:] + word2[minlen:]
        result = ''.join(result) + rest
        return result
