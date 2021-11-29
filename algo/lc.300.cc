class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        if (nums.empty()) return 0;
        
        // g(i) = max /  1 + max_{j=1}^{i-1} g(j) if a_i > a_j
        //            \  1  forall j a_i <= a_j
        // f(i) = max [ g[j] for j in 0:i ] 
        vector<int> g (nums.size(), 0);
        g[0] = 1;
        for (int i = 1; i < nums.size(); i++) {
            int max1toim1 = 0;
            for (int j = 0; j < i; j++) {
                if (nums[i] > nums[j])
                    max1toim1 = max(max1toim1, g[j]);
            }
            g[i] = 1 + max1toim1;
        }
        // find the max g(i)
        int ret = INT_MIN;
        for (auto i : g) ret = max(ret, i);
        return ret;
    }
};
