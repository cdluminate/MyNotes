class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        if (grid.empty()) return 0;
        
        int rows = grid.size();
        int cols = grid.front().size();
        
        // first row and first col
        for (int j = 1; j < cols; j++) grid[0][j] += grid[0][j-1];
        for (int i = 1; i < rows; i++) grid[i][0] += grid[i-1][0];
        
        // the rest part
        for (int i = 1; i < rows; i++) {
            for (int j = 1; j < cols; j++) {
                grid[i][j] += (grid[i-1][j] < grid[i][j-1]) ? grid[i-1][j] : grid[i][j-1];
            }
        }
        return grid[rows-1][cols-1];
    }
};
