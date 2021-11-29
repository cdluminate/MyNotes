# Tag: array

class Solution(object):
    def twoSum(self, numbers, target):
        """
        :type numbers: List[int]
        :type target: int
        :rtype: List[int]
        """
        # first pass, setup cache O(n)
        d = {}
        for i,v in enumerate(numbers):
            d[v]=i
        # second pass, find solution O(n)
        for i,v in enumerate(numbers):
            if target-v in d:
                return [i+1, d[target-v]+1]
        return [-1,-1]

