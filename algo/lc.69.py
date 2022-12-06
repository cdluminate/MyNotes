class Solution:
    def mySqrt(self, x: int) -> int:
        right = x // 2 if x > 1 else 1
        while True:
            if right * right > x:
                if (right // 2) * (right // 2) > x:
                    right = right // 2
                else:
                    right = right - 1
            else: # right * right <= x:
                return right
