class Solution:
    def countBits(self, n: int) -> List[int]:
        def helper(n: int) -> int:
            # find the number of "1" bits
            tally = 0
            while n > 0:
                tally += n % 2
                n = n // 2
            return tally
        results = []
        for i in range(n+1):
            results.append(helper(i))
        return results

