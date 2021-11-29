class Solution(object):
    def getRow(self, rowIndex):
        """
        :type rowIndex: int
        :rtype: List[int]
        """
        def xConv(s): # conv(s, [1,1])
            sp = []
            for i in range(len(s)-1):
                sp.append(s[i]+s[i+1])
            return [1]+sp+[1]
        signal = [1]
        for i in range(rowIndex):
            signal = xConv(signal)
        return signal
