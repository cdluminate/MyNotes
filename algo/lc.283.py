class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        read_cursor = 0
        write_cursor = 0
        while read_cursor < n:
            if nums[read_cursor] != 0:
                nums[write_cursor] = nums[read_cursor]
                write_cursor += 1
            # seek for the next
            read_cursor += 1
        for i in range(write_cursor, n):
            nums[i] = 0

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
        
