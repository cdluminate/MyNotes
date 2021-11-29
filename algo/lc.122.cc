class Solution {
public:
    int maxProfit(vector<int>& prices) {
        if (prices.empty()) return 0;
        
        // accuProfit(i) = accuProfit(i-1) + max{0, p(i)-p(i-1)}
        int accuProfit = 0;
        for (int i = 1; i < prices.size(); i++) {
            accuProfit += max(0, prices[i] - prices[i-1]);
        }
        return accuProfit;
    }
};
