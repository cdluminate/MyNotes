class Solution:

    def dot(self, a, b) -> float:
        assert len(a) == len(b)
        return sum([x * y for x, y in zip(a, b)])

    def findMaxAverage(self, nums: List[int], k: int) -> float:
        if k > len(nums):
            return 0.0
        if len(nums) == 1 == k:
            return nums[0]
        # conv1_valid(nums, kernel=[1] * k)
        results = []
        kernel = [1/k] * k
        for i in range(len(nums) - k + 1):
            j = i + k
            tmp = self.dot(nums[i:j], kernel)
            results.append(tmp)
            #print(i, j, tmp)
        return max(results)
