class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0
        elif len(nums) == 1:
            return nums[0]
        else:
            dp = [nums[0]]
            for (i, x) in enumerate(nums):
                if i == 0:
                    continue
                # dp[i] = max{x_i, x_1+dp[i-1]}
                val_include = x + dp[-1]
                val_exclude = x
                dp.append(max(val_include, val_exclude))
            return max(dp)
            
