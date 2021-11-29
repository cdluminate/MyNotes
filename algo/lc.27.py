class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        '''
        total = len(nums)
        cur = 0
        while cur < total:
            if nums[cur] == val:
                nums.pop(cur)
                cur -= 1
                total -= 1
            cur += 1
        return len(nums)
        '''
        if not nums: return 0
        
        idx = 0
        for i, v in enumerate(nums):
            if v != val:
                nums[idx] = v
                idx += 1
        return idx
