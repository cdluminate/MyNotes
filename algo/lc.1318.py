class Solution:
    def minFlips(self, a: int, b: int, c: int) -> int:
        # convert to List[int]
        a = list(map(int, list(bin(a))[2:]))
        b = list(map(int, list(bin(b))[2:]))
        c = list(map(int, list(bin(c))[2:]))
        # pad them to maximum length
        maxlen = max(len(a), len(b), len(c))
        while len(a) != maxlen:
            a.insert(0, 0)
        while len(b) != maxlen:
            b.insert(0, 0)
        while len(c) != maxlen:
            c.insert(0, 0)
        # traverse the bits
        tally = 0
        for i in range(maxlen):
            if c[i] == 0:
                # both a[i] and b[i] have to be 0
                tally += a[i] + b[i]
            else: # c[i] == 1:
                if a[i] + b[i] > 0:
                    pass # no change
                else:
                    tally += 1 # flip one of them
        return tally
