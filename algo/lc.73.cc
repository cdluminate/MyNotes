class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        // masking
        vector<bool> maskrow(matrix.size(), false);
        vector<bool> maskcol(matrix[0].size(), false);
        for (int i = 0; i < matrix.size(); i++) {
            for (int j = 0; j < matrix[0].size(); j++) {
                if (matrix[i][j] == 0){
                    maskrow[i] = true;
                    maskcol[j] = true;
                }
            }
        }
        
        // zeroing
        for (int i = 0; i < matrix.size(); i++) {
            for (int j = 0; j < matrix[0].size(); j++) {
                if (true == maskrow[i] || true == maskcol[j])
                    matrix[i][j] = 0;
            }
        }
        return; // O(n^2), S(m+n)
    }
};
