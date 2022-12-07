class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        if not nums:
            return []
        elif len(nums) == 1:
            return [[], nums]
        else:
            return [[] + x for x in self.subsets(nums[1:])] + \
                   [[nums[0]] + x for x in self.subsets(nums[1:])]
