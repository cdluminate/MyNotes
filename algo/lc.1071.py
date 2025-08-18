import math
class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        if str1 + str2 != str2 + str1:
            return ''
        gcd = math.gcd(len(str1), len(str2))
        return str1[:gcd]

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        if len(str1) == len(str2):
            return str1 if str1 == str2 else ''
        minlen = min(len(str1), len(str2))
        maxlen = max(len(str1), len(str2))
        shortone = min([str1, str2], key=lambda x: len(x))
        longone = max([str1, str2], key=lambda x: len(x))
        print(minlen, shortone, maxlen, longone)
        maxgcd = ''
        for i in range(1, minlen+1):
            probe = shortone[:i]
            isgcdmax = (probe * (maxlen // i)) == longone
            isgcdmin = (probe * (minlen // i)) == shortone
            if isgcdmax and isgcdmin:
                maxgcd = probe
            print(i, probe, isgcdmax, isgcdmin)
        return maxgcd
