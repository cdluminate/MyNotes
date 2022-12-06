class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        d = {}
        for (i, x) in enumerate(nums):
            if (target - x) not in d.keys():
                d[x] = i
            else:
                return [d[target - x], i]
