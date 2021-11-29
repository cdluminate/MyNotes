class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # non-empty, majority element always exist
        total = len(nums)
        d = {}
        for i in nums:
            if i in d.keys():
                d[i] += 1
            else:
                d[i] = 1
            if d[i] > total/2: return i
        return -1
