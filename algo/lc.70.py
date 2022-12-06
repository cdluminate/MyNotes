class Solution:
    cache = {0: 1, 1:1}
    def climbStairs(self, n: int) -> int:
        if n in (0, 1):
            return 1
        else:
            if n in self.cache:
                return self.cache[n]
            else:
                nfact = self.climbStairs(n-1) + self.climbStairs(n-2)
                self.cache[n] = nfact
                return nfact

class Solution:
    def climbStairs(self, n: int) -> int:
        if n in (0, 1):
            return 1
        else:
            l = [1, 1]
            for i in range(2,n+1):
                l.append(l[i-1] + l[i-2])
            return l[-1]
