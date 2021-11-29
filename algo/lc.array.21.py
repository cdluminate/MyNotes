class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if len(nums) == 0: return 0
        idx = 1
        for i in range(1, len(nums)):
            if nums[i] > nums[idx-1]:
                nums[idx] = nums[i]
                idx += 1
        return idx

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums: return 0
        idx = 0
        for j in nums:
            if j != nums[idx]:
                idx += 1
                nums[idx] = j
        return idx+1
