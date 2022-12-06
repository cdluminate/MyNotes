class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        if not nums1 and not nums2:
            return []
        elif not nums1 or not nums2:
            return nums2 if not nums2 else nums1
        # else
        for cur2 in range(n):
            # where to insert nums2[cur2]
            cur1 = 0
            while nums2[cur2] >= nums1[cur1] and cur1 < m + cur2:
                cur1 = cur1 + 1
            nums1.insert(cur1, nums2[cur2])
            nums1.pop(-1)
