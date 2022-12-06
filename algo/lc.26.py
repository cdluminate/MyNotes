class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        cursor = None
        nodup = 0
        for (i, n) in enumerate(nums):
            if n != cursor:
                nums[nodup] = n
                nodup = nodup + 1
                cursor = n
            else:
                pass
        return nodup
