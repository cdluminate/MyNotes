# [array]
class Solution(object):
    def arrayPairSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        s = sorted(nums, reverse=True)
        return sum([s[i] for i in range(len(s)) if i%2==1])
