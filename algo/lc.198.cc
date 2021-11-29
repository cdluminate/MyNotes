class Solution {
public:
    int rob(vector<int>& nums) {
        if (nums.empty()) return 0;
        
        vector<int> dp (nums.size(), 0);
        for (int i = 0; i < nums.size(); i++) {
            if (i==0) {
                dp[i] = nums[0];
            } else if (i==1) {
                dp[i] = nums[0]>nums[1] ? nums[0] : nums[1];
            } else {
                dp[i] = max(nums[i] + dp[i-2], dp[i-1]);
            }
        }
        return dp[nums.size()-1];
    }
};
