import math

def gcd(a: int, b: int) -> int:
    minval = min(a, b)
    maxval = max(a, b)
    if minval == 0:
        return maxval
    elif maxval % minval == 0:
        return minval
    else:
        return gcd(minval, maxval % minval)

assert math.gcd(12, 15) == gcd(12, 15)
assert math.gcd(100, 25) == gcd(100, 25)
assert math.gcd(100, 0) == gcd(100, 0)
assert math.gcd(0, 100) == gcd(0, 100)
assert gcd(1071, 462) == 21
