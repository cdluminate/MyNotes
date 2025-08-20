class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        if 0 not in nums:
            # we must delete a 1
            return max(0, len(nums) - 1)
        # elastic sliding window from left to right
        maxnum = 0 # result
        numzero = 0 # tmp for state
        left = 0 # cursor, inclusive
        right = 0 # cursor, exclusive
        while left < len(nums) and right < len(nums):
            #print('state', 'left=', left, 'right=', right, 'max=', maxnum, '0=', numzero)
            if nums[right] == 1:
                right += 1 # expand right
                maxnum = max(right - left, maxnum) # update value
            elif nums[right] == 0 and numzero == 0:
                # keep expanding right and cross the current zero
                numzero, right = 1, right+1
                maxnum = max(right - left, maxnum) # update value
            elif nums[right] == 0 and numzero > 0:
                # shrink left
                numzero -= 1 if nums[left] == 0 else 0
                left += 1
            else:
                raise Exception("should not happen")
        return maxnum - 1

class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        if 0 not in nums:
            return max(0, len(nums) - 1)
        maxnum = 0
        for delidx in range(len(nums)):
            if nums[delidx] == 1:
                continue
            else:
                # delete the 0 and obain the max sub
                state = 0
                maxsub = 0
                for i in range(len(nums)):
                    if i == delidx:
                        continue
                    elif nums[i] == 1:
                        state += 1
                        if state > maxsub:
                            maxsub = state
                    else: # nums[i] == 0:
                        state = 0
                if maxsub > maxnum:
                    maxnum = maxsub
        return maxnum

class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        if 0 not in nums:
            return max(0, len(nums)-1)
        maxnum = 0
        for i in range(len(nums)):
            if nums[i] == 1:
                continue
            else:
                removei = list(nums)
                _ = removei.pop(i)
                tmp: str = ''.join(str(x) for x in removei)
                maxsub = max([len(x) for x in tmp.split('0')])
                if maxsub > maxnum:
                    maxnum = maxsub
        return maxnum

class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        maxnum = 0
        for i in range(len(nums)):
            removei = list(nums)
            _ = removei.pop(i)
            tmp: str = ''.join(str(x) for x in removei)
            maxsub = max([len(x) for x in tmp.split('0')])
            if maxsub > maxnum:
                maxnum = maxsub
        return maxnum
