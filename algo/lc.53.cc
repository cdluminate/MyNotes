class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        if (nums.empty()) return 0;
        
		// DP: g(i) = max{ a_i, g(i-1) + a_i }
		//     f(i) = max_{j=1}^i g(j)
        vector<int> f(nums.size(), 0);
        f[0] = nums[0];
        for (int i = 1; i < nums.size(); i++) {
            f[i] = max(f[i-1]+nums[i], nums[i]);
        }
        int max = INT_MIN;
        for (int i : f) max = (i > max) ? i : max;
        return max;
    }
};
