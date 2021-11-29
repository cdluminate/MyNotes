class Solution(object):
    def maximumProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        li = sorted(nums, reverse=True)
        pa = li[0]*li[1]*li[2]
        pb = li[0]*li[-1]*li[-2]
        return pa if pa>pb else pb
