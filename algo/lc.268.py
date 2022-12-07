class Solution(object):
    def missingNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # first pass: create cache
        d = {}
        for i in nums:
            d[i] = 1
        # second pass: scan for the missing one
        for i in range(len(nums)+1):
            if i not in d:
                return i
        return -1

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        d = {x: True for x in nums}
        for i in range(len(nums)+1):
            if i not in d:
                return i
        return -1
