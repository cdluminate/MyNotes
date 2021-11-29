class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        if (coins.empty()) return 0;
        
        vector<int> dp(amount+1, amount+1); // INT_MAX .. int overflow
        dp[0] = 0;
        for (int i = 0; i < amount+1; i++) {
            for (int j = 0; j < coins.size(); j++) {
                if (i >= coins[j]) {
                    dp[i] = min(dp[i], 1 + dp[i - coins[j]]);
                }
            }
        }
        return (dp[amount] > amount) ? -1 : dp[amount];
    }
};
