class Solution(object):
    def containsNearbyDuplicate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """
        #if len(nums)<=k:
        #    return len(nums)!=len(list(set(nums)))
        #else:
        #    for i in range(len(nums)-k):
        #        if len(nums[i:i+k+1])!=len(list(set(nums[i:i+k+1]))):
        #            return True
        #    return False
        # ^ Time out
        lastpos = {}
        for i,v in enumerate(nums):
            if v not in lastpos: # if v not in lastpos.keys() # Time out
                lastpos[v] = i
            else:
                if abs(lastpos[v] - i) <= k:
                    return True
                else:
                    lastpos[v] = i
        return False
