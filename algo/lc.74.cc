class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        if (matrix.empty()) return false;
        
        int m = matrix.size();
        int n = matrix.front().size();
        
        int curl = 0;
        int curr = m*n-1; // not m*n-1
        auto cur2row = [&n](int x){ return (int)x/n; };
        auto cur2col = [&n](int x){ return x%n; };
        
        while(curl <= curr) {
            int mid = (curr+curl)/2;
            int curv = matrix[cur2row(mid)][cur2col(mid)];
            if (curv == target) {
                return true;
            } else if (curv < target) {
                curl = mid+1;
            } else { // value > target
                curr = mid-1;
            }
        }
        return false;
    }
};
