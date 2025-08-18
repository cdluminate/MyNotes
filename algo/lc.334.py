class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        if len(nums) < 3:
            return False
        bar1, bar2 = max(nums), max(nums)+1
        for n in nums:
            if n <= bar1:
                bar1 = n
            elif bar1 < n <= bar2:
                bar2 = n
            elif n > bar2:
                return True
            else:
                raise Exception
        return False
