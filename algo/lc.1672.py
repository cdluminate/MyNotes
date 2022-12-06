class Solution:
    def maximumWealth(self, accounts: List[List[int]]) -> int:
        sums = [sum(x) for x in accounts]
        return max(sums)
