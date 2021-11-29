class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        d = {}
        for (i, n) in enumerate(nums):
            idx = d.get(target - n)
            if idx is not None:
                return [idx, i]
            d[n] = i
        return []
