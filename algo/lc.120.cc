class Solution {
public:
    int minimumTotal(vector<vector<int>>& triangle) {
        helper(triangle, 0);
        return triangle[0][0];
    }
    void helper(vector<vector<int> >& triangle, int currow) {
        if (currow == triangle.size()-1) {
            return;
        } else {
            helper(triangle, currow+1);
            for (int j = 0; j < triangle[currow].size(); j++) {
                triangle[currow][j] += min(triangle[currow+1][j], triangle[currow+1][j+1]);
            }
        }
    }
};
