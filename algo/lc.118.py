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


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        if numRows == 0:
            return []
        # numRows > 0
        tri = []
        for i in range(1, numRows+1):
            row = []
            for j in range(i):
                if j == 0 or j == i-1:
                    row.append(1)
                else:
                    a = tri[i-2][j-1]
                    b = tri[i-2][j]
                    row.append(a + b)
            tri.append(row)
        return tri
