class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        # mincumcost[i] = min(mincumcost[i-1] + cost[i],
        #                     mincumcost[i-2] + cost[i])
        if not cost:
            # length 0
            return 0
        elif len(cost) == 1:
            # length 1
            return cost[0]
        else:
            # length >= 2
            dp = [cost[0], cost[1]]
            for i in range(2, len(cost)):
                dp.append(min(dp[i-1] + cost[i], dp[i-2] + cost[i]))
            return min(dp[-1], dp[-2])
