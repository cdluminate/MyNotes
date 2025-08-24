class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:

        def requires(pile: int, speed: int) -> int:
            return (pile // speed) + (0 if pile % speed == 0 else 1)

        def enough(speed: int):
            req = [requires(x, speed) for x in piles]
            #print('enough?>', req, h, sum(req) <= h)
            return sum(req) <= h

        # obvious cases
        if len(piles) == h:
            return max(piles)
        if len(piles) > h:
            return -1 # no solution for this case

        # we should conduct a binary search
        minspeed = max(piles)
        left, right = 1, max(piles)
        while left <= right:
            mid = left + (right - left) // 2
            # case: mid is still enough to finish all
            if enough(mid):
                minspeed = mid
                left, right = left, mid - 1
            # case: mid is not enough to finish all
            else:
                left, right = mid + 1, right

        return minspeed

