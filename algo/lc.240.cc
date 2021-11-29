class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        if (matrix.empty()) return false;
        
        int rows = matrix.size();
        int cols = matrix.front().size();
        int currow = 0, curcol = cols-1;
        while (currow < rows && curcol >= 0) {
            if (target == matrix[currow][curcol])
                return true;
            else if (target > matrix[currow][curcol])
                currow++;
            else // target < ...
                curcol--;
        }
        return false;
    }
};
