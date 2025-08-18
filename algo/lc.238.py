class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        if not nums:
            return []
        # cumulative product left to right
        cumprodltr = [nums[0]]
        for x in nums[1:]:
            cumprodltr.append(cumprodltr[-1] * x)
        # cumulative product right to left
        cumprodrtl = [nums[-1]]
        for x in nums[:-1][::-1]:
            cumprodrtl.insert(0, cumprodrtl[0] * x)
        # combine
        results = []
        for i in range(len(nums)):
            left = cumprodltr[i-1] if i > 0 else 1
            right = cumprodrtl[i+1] if i < len(nums) - 1 else 1
            results.append(left * right)
        return results
