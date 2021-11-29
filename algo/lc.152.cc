class Solution {
public:
    int maxProduct(vector<int>& nums) {
        if (nums.empty()) return 0;
        
        /* gmax(i) = max{a_i, a_i*gmax(i-1), a_i*gmin(i-1)}
           gmin(i) = min{a_i, a_i*gmax(i-1), a_i*gmin(i-1)}
           g(i)    = max{a_i, a_i*gmax(i-1), a_i*gmin(i-1)}
           f(i)    = max_{j=1}^i g(j)
         */
#define MAX(a,b,c) (max(a, max(b, c)))
#define MIN(a,b,c) (min(a, min(b, c)))
        vector<int> gmax (nums.size(), INT_MIN);
        vector<int> gmin (nums.size(), INT_MAX);
        vector<int> g    (nums.size(), INT_MIN);
        gmax[0] = nums[0];
        gmin[0] = nums[0];
        g[0]    = nums[0];
        for (int i = 1; i < nums.size(); i++) {
            gmax[i] = MAX(nums[i], nums[i]*gmax[i-1], nums[i]*gmin[i-1]);
            gmin[i] = MIN(nums[i], nums[i]*gmax[i-1], nums[i]*gmin[i-1]);
            g[i]    = MAX(nums[i], nums[i]*gmax[i-1], nums[i]*gmin[i-1]);
        }
        // find the max g(j)
        int ret = INT_MIN;
        for (auto i : g) ret = max(ret, i);
        return ret;
    }
};
