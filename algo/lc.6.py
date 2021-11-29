class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        # calculate group size
        if numRows == 1:
          gsize = 1
        else:
          gsize = (numRows-1)*2
        # generate empty rows
        rows = [ [] for i in range(numRows) ]
        # scan string and append into rows
        for (k,char) in enumerate(list(s)):
          # calculate local id \in [ 0, gsize )
          lid = ((k+1)%gsize - 1)%gsize
          if lid <= numRows-1:
            # lid \in [0, numRows)
            rows[lid].append(char)
          else:
            lidcomp = numRows-1 - (lid+1-numRows)
            rows[lidcomp].append(char)
        # assemble string
        return ''.join([ ''.join(row) for row in rows ])

solution = Solution()
print(solution.convert("PAYPALISHIRING", 3))

# accepted
