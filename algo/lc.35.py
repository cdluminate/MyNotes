class Solution(object):
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        # x in list(int) : O(n)
        # we'd better solve this within a single pass
        if len(nums)==0: return 0
        if target <= nums[0]:
            return 0
        if len(nums)==1: return 1
        for i in range(1,len(nums)):
            a, b = nums[i-1], nums[i]
            if target <= b: return i
        return len(nums)
