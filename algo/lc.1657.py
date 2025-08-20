from collections import Counter
class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        if len(word1) != len(word2):
            return False
        if word1 == word2:
            return True
        # operation 1+2: order invariant
        #.               key-invariant, same counter
        uniq1, uniq2 = set(word1), set(word2)
        if uniq1 != uniq2:
            return False
        counter1, counter2 = Counter(word1), Counter(word2)
        c1 = list(sorted(counter1.values()))
        c2 = list(sorted(counter2.values()))
        if c1 != c2:
            return False
        return True
