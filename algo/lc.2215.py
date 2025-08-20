class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        uniq1 = set(nums1)
        uniq2 = set(nums2)
        ans1 = [x for x in uniq1 if x not in uniq2]
        ans2 = [x for x in uniq2 if x not in uniq1]
        return [ans1, ans2]
