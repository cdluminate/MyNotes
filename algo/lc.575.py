class Solution:
    def distributeCandies(self, candies):
        """
        :type candies: List[int]
        :rtype: int
        """
        kinds = len(set(candies))
        numbers = len(candies)
        return min(int(kinds), int(numbers/2));
