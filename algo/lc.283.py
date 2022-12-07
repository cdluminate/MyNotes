class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        wtcursor = 0
        rdcursor = 0
        while rdcursor < len(nums):
            if nums[rdcursor] != 0:
                nums[wtcursor] = nums[rdcursor]
                if wtcursor != rdcursor:
                    nums[rdcursor] = 0
                wtcursor += 1
                rdcursor += 1
            else: # == 0
                rdcursor += 1
        
