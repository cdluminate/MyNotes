class Solution {
public:
    int climbStairs(int n) {
        // fibonacci
        int prev = 0;
        int cur = 1;
        for (int i = 0; i < n; i++) {
            int tmp = cur;
            cur += prev;
            prev = tmp;
        }
        return cur;
    }
};
