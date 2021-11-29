# array
# reshape a matrix

a = [[1,2],[3,4]]

def reshape(mat, r, c):
    # verify matrix size
    ro = len(mat)
    co = len(mat[0])
    if ro*co != r*c: return mat
    # serialize matrix into list
    pool = [mat[i][j] for i in range(ro) for j in range(co)]
    res = []
    for i in range(r):
        res.append(pool[:c])
        pool = pool[c:]
    return res

print(reshape(a,1,4))


class Solution(object):
    def matrixReshape(self, nums, r, c):
        """
        :type nums: List[List[int]]
        :type r: int
        :type c: int
        :rtype: List[List[int]]
        """
        # verify matrix size
        mat=nums
        ro = len(mat)
        co = len(mat[0])
        if ro*co != r*c: return mat
        # serialize matrix into list
        pool = [mat[i][j] for i in range(ro) for j in range(co)]
        res = []
        for i in range(r):
            res.append(pool[:c])
            pool = pool[c:]
        return res
