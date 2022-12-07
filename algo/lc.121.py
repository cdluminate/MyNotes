class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) < 2:
            return 0
        # at least two numbers
        maxprofit = 0
        lowp = max(prices)
        for x in prices:
            if x < lowp:
                lowp = x
            if x - lowp > maxprofit:
                maxprofit = x - lowp
        return maxprofit
