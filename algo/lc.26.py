class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        '''
        if len(nums)==0:
            return 0
        prev = nums[0]
        total = len(nums)
        cur = 1
        while cur<total:
            if nums[cur] == prev:
                nums.pop(cur)
                cur -= 1
                total -= 1
            prev = nums[cur]
            cur += 1
        return len(nums)
        '''
        if not nums:
            return 0
        idx = 0
        for i,v in enumerate(nums):
            if v != nums[idx]:
                idx += 1
                nums[idx] = v
        return idx+1
