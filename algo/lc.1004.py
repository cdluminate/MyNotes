class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        if sum(i == 0 for i in nums) <= k:
            return len(nums)
        # elastic sliding window
        maxnum = 0 # result
        numzero = 0 # state
        left = 0 # cursor, inclusive
        right = 0 # cursor, exclusive
        while left < len(nums) and right < len(nums):
            #print('state', left, right, numzero, maxnum)
            if nums[right] == 1:
                # expand right
                right += 1
                maxnum = max(right - left, maxnum)
            elif nums[right] == 0 and numzero < k:
                # expand right, count zero
                right += 1
                numzero += 1
                maxnum = max(right - left, maxnum)
            elif nums[right] == 0 and numzero >= k:
                # shrink left, reduce count
                if nums[left] == 0:
                    numzero -= 1
                left += 1
            else:
                raise Exception("should not happen")
        return maxnum
