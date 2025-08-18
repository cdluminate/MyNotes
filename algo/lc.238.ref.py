class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        if not nums:
            return []
        # postfix product
        postfix = []
        tmp = 1
        for i in range(len(nums)-1, -1, -1):
            postfix.append(tmp)
            tmp *= nums[i]
        postfix = postfix[::-1]
        # prefix & result
        results = []
        tmp = 1
        for (i, x) in enumerate(nums):
            results.append(tmp * postfix[i])
            tmp *= x
        return results
            
