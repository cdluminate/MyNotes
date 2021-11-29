class Solution(object):
    def findDisappearedNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        s = set(nums)
        if len(s)==0: return []
        nmax = len(nums) #max(s)
        dropped = []
        for i in range(1,nmax+1):
            if i not in s: dropped.append(i)
        return dropped
