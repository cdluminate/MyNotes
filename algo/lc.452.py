class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        # case: no input
        if not points:
            return 0
        # case: one input
        if len(points) == 1:
            return 1
        # find the non-overlapping segments
        result = 0
        state = -int(2**31)-1
        points.sort(key=lambda x: x[1])
        for (i, j) in points:
            # case 1: no overlap
            if state < i:
                result += 1
                state = j
            # case 2: there is overlap
            else:
                pass
        return result
