class Solution:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        # free: profit, end of day without stock
        # hold: profit, end of day holding stock
        free = [None for _ in prices]
        hold = [None for _ in prices]
        # initialize first day
        free[0], hold[0] = 0, -prices[0]
        for i in range(1, len(prices)):
            # free: either no op or sell the stock
            free[i] = max(free[i-1], hold[i-1] + prices[i] - fee)
            # hold: either no op or buy the stock
            hold[i] = max(hold[i-1], free[i-1] - prices[i])
        return free[-1]

class Solution:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        N = len(prices) + 1
        # initialize dp matrix
        dp = [[(None, None) for _ in range(N)] for _ in range(N)]
        dp[0][0] = (0, None) # (profit, onhold)
        for i in range(N):
            for j in range(N):
                # skip the initialization
                if i == j == 0:
                    continue
                # go right is buy:
                # 1. if the previous state is none, update state
                # 2. if the previous state is not none, no np
                if j - 1 < 0:
                    # not possible to buy
                    buy = (0, None)
                elif dp[i][j-1][1] is not None:
                    # not possible to buy, no op and copy
                    buy = dp[i][j-1]
                else:
                    # buy in
                    buy = [dp[i][j-1][0] - fee, prices[i-1]]
                # go down is sell:
                # 1. if the previous state is none, no op
                # 2. if the previous state is not none, update profit
                if i - 1 < 0:
                    # not possible to sell
                    sell = (0, None)
                elif dp[i-1][j][1] is not None:
                    # sell out, and apply the fee deduction
                    profit = dp[i-1][j][0] + prices[j-1] - dp[i-1][j][1] - fee
                    sell = (profit, None)
                else:
                    # not possible to sell, no op and copy
                    sell = dp[i-1][j]
                # go along diagonal (south east) is no op:
                # 1. just copy profit and state
                if i-1<0 or j-1<0:
                    # index out of range:
                    noop = (0, None)
                else:
                    noop = dp[i-1][j-1]
                # dp[i][j] = max(buy, sell, noop, key=lambda x: x[0])
                best = max([buy, sell, noop], key=lambda x: x[0])
                dp[i][j] = best
        return dp[-1][-1][0]
