class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = left + (right - left) // 2
            leftOK = True if mid-1<0 else nums[mid-1]<nums[mid]
            rightOK = True if mid+1>len(nums)-1 else nums[mid]>nums[mid+1]
            if leftOK and rightOK:
                # we hit a peak
                return mid
            elif leftOK:
                # there is a peak on the right side
                left, right = mid+1, right
            elif rightOK:
                # there is a peak on the left side
                left, right = left, mid-1
            else:
                # either directions should be good
                left, right = mid+1, right

class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        n = len(nums)
        # build the right prefix, i-th means nums[i] > nums[i+1]
        right = [nums[i] > nums[i+1] for i in range(n-1)] + [True]
        # build the left prefix, i-th means nums[i-1] < nums[i]
        left = [True] + [nums[i-1] < nums[i] for i in range(1, n)]
        # scan from left to right
        for i in range(n):
            if left[i] and right[i]:
                return i
