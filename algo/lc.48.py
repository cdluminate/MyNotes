class Solution:
    def transpose(self, matrix: List[List[int]]) -> None:
        '''
        in-place transpose
        '''
        N = len(matrix)
        for i in range(N):
            for j in range(i):
                tmp = matrix[i][j]
                matrix[i][j] = matrix[j][i]
                matrix[j][i] = tmp
    def lrflip(self, matrix: List[List[int]]) -> None:
        N = len(matrix)
        for i in range(N):
            for j in range(N // 2):
                tmp = matrix[i][j]
                matrix[i][j] = matrix[i][N-j-1]
                matrix[i][N-j-1] = tmp
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        self.transpose(matrix)
        self.lrflip(matrix)
