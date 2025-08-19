class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        elif len(nums) == 1:
            return nums[0]
        else:
            # length >= 2
            dp = [nums[0], max(nums[1], nums[0])]
            for i in range(2, len(nums)):
                dpi = max(dp[i-1], dp[i-2] + nums[i])
                dp.append(dpi)
            return dp[-1]
