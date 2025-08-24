class Solution:
    cache = {}
    def minDistance(self, word1: str, word2: str) -> int:
        if (word1, word2) in self.cache:
            return self.cache[(word1, word2)]
        # case: boundary -> no edit
        if word1 == word2:
            res = 0
        # case: one of them is empty -> simple add/delete
        elif not word1 or not word2:
            res = abs(len(word1) - len(word2))
        # case: first word matches, no op
        elif word1[0] == word2[0]:
            res = self.minDistance(word1[1:], word2[1:])
        # case: first word does not match, try all ops
        else:
            # op1: insert word2[0] to word1
            op1 = 1 + self.minDistance(word1, word2[1:])
            # op2: delete word1[0]
            op2 = 1 + self.minDistance(word1[1:], word2)
            # op3: replace word1[0] into word2[0]
            op3 = 1 + self.minDistance(word1[1:], word2[1:])
            # find the minimum op
            res = min(op1, op2, op3)
        # cache the result and return
        self.cache[(word1, word2)] = res
        return res

class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        # case: boundary -> no edit
        if word1 == word2:
            return 0
        # case: one of them is empty -> simple add/delete
        elif not word1 or not word2:
            return abs(len(word1) - len(word2))
        # case: first word matches, no op
        elif word1[0] == word2[0]:
            return self.minDistance(word1[1:], word2[1:])
        # case: first word does not match, try all ops
        else:
            # op1: insert word2[0] to word1
            op1 = 1 + self.minDistance(word1, word2[1:])
            # op2: delete word1[0]
            op2 = 1 + self.minDistance(word1[1:], word2)
            # op3: replace word1[0] into word2[0]
            op3 = 1 + self.minDistance(word1[1:], word2[1:])
            # find the minimum op
            return min(op1, op2, op3)
