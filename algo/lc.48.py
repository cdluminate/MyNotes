class Solution(object):
    def rotate(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: void Do not return anything, modify matrix in-place instead.
        """
        M, N = len(matrix), len(matrix[0]) # this should be a square matrix
        
        # first pass: transpose
        for i in range(M):
            for j in range(i, N):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        
        # second pass: mirroring left-right
        for i in range(M):
            matrix[i].reverse()
