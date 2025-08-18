class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        result = []
        maxval = max(candies)
        for x in candies:
            if x + extraCandies >= maxval:
                result.append(True)
            else:
                result.append(False)
        return result
