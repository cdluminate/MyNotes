from collections import defaultdict
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        # first pass: build the value -> index dictionary
        val2idx = defaultdict(int)
        for (i, x) in enumerate(nums):
            val2idx[x] += 1
        # second pass: traverse numbers and consume the dictionary
        result = 0
        for n in nums:
            if (k - n) in val2idx and val2idx[k - n] > 0:
                val2idx[k - n] -= 1
                result += 1
        # we actually used possible combinations twice
        return result // 2


from collections import defaultdict
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        # first pass: build the value -> index dictionary
        val2idx = defaultdict(list)
        for (i, x) in enumerate(nums):
            val2idx[x].append(i)
        # second pass: traverse numbers and consume the dictionary
        result = 0
        for n in nums:
            if (k - n) in val2idx and val2idx[k - n]:
                val2idx[k - n].pop()
                result += 1
        # we actually used possible combinations twice
        return result // 2
