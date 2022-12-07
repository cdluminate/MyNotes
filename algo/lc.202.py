class Solution:
    def isHappy(self, n: int) -> bool:
        previous = []
        x = n
        while True:
            sumsq = sum(int(x)**2 for x in str(x))
            if sumsq == 1:
                return True
            else:
                if sumsq in previous:
                    return False
                else:
                    previous.append(sumsq)
                    x = sumsq
