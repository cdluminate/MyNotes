class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        # counter 1
        d1 = dict()
        for x in nums1:
            if x in d1:
                d1[x] += 1
            else:
                d1[x] = 1
        # counter 2
        d2 = dict()
        for x in nums2:
            if x in d2:
                d2[x] += 1
            else:
                d2[x] = 1
        # merge
        ret = []
        for k in set(d1.keys()).union(set(d2.keys())):
            if (k in d1) and (k in d2):
                ret.extend([k] * min(d1[k], d2[k]))
        return ret
