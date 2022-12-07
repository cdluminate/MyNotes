class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        if not nums:
            return []
        elif len(nums) == 1:
            return [nums]
        else:
            res = []
            for i in range(len(nums)):
                copy = list(nums)
                x = copy.pop(i)
                perms = self.permute(copy)
                perms = [[x] + p for p in perms]
                res.extend(perms)
            return res
