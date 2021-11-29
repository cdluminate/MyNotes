class Solution {
public:
    int numSquares(int n) {
        if (n <= 0) return 0;
        
        /* // DP, slow
        vector<int> dp (n+1, INT_MAX);
        dp[0] = 0;
        for (int i = 1; i <= n; i++) {
            // calculate dp[i]
            for (int j = 1; j*j <= i; j++) {
                dp[i] = min(dp[i], dp[i - j*j] + 1);
            }
        }
        return dp.back();
        */
        
		// static DP
        static vector<int> dp {0};
        while (dp.size() < n+1) {
            int i = dp.size();
            int dpi = INT_MAX;
            for (int j = 1; j*j <= i; j++) {
                dpi = min(dpi, dp[i - j*j] + 1);
            }
            dp.push_back(dpi);
        }
        return dp[n];

		// think also BFS
    }
};
