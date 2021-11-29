class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        int s = matrix.size();
        
        // frist pass: transpose
        for (int i = 0; i < s; i++) {
            for (int j = 0; j < i; j++) {
                int tmp = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = tmp;
            }
        }
        
        // second pass: flipping left-right
        for (int i = 0; i < s; i++) {
            for (int j = 0; j < s/2; j++) {
                int tmp = matrix[i][j];
                matrix[i][j] = matrix[i][s-1-j];
                matrix[i][s-1-j] = tmp;
            }
        }
    }
};
