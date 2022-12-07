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

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        length = len(nums)
        d = dict()
        for x in nums:
            if x in d:
                d[x] = d[x] + 1
            else:
                d[x] = 1
            if d[x] > length // 2:
                return x
