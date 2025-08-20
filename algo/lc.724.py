class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        # first pass: right to left cumulative sum
        rightcumsum = [0]
        for i in range(len(nums)-1, 0, -1):
            tmp = rightcumsum[-1] + nums[i]
            rightcumsum.append(tmp)
        rightcumsum = rightcumsum[::-1]
        # second pass: left to riht cumulative sum
        leftcumsum = 0
        for i in range(len(nums)):
            if leftcumsum == rightcumsum[i]:
                return i
            else:
                leftcumsum += nums[i]
        return -1

class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        # first pass: right to left cumulative sum
        rightcumsum = [0]
        for i in range(len(nums)-1, 0, -1):
            tmp = rightcumsum[0] + nums[i]
            rightcumsum.insert(0, tmp)
        assert len(rightcumsum) == len(nums)
        # second pass: left to riht cumulative sum
        leftcumsum = 0
        for i in range(len(nums)):
            if leftcumsum == rightcumsum[i]:
                return i
            else:
                leftcumsum += nums[i]
        return -1
