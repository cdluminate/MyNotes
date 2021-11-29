class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        #return [ (x-k)%len(nums) for x in nums ]
        for i in range(k):
            #nums.append(nums.pop(0)) # move left
            nums.insert(0, nums.pop()) # move right
