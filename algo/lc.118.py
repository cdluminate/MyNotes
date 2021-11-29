class Solution(object):
    def generate(self, numRows):
        """
        :type numRows: int
        :rtype: List[List[int]]
        """
        # first pass: empty triangle
        tria = [
            [0 for j in range(i+1)] for i in range(numRows)
        ]
        print(tria)
        # second pass: fill in values
        for i,iline in enumerate(tria):
            iline[0] = 1
            iline[-1] = 1
            if i>1:
                for j in range(1,len(iline)-1):
                    iline[j] = tria[i-1][j-1] + tria[i-1][j]
        return tria
