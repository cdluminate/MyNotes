class Solution {
public:
    int maxProfit(vector<int>& prices) {
        if (prices.empty()) return 0;
        
        /*
        int maxdiff = 0;
        for (int i = 0; i < prices.size(); i++) {
            for (int j = i+1; j < prices.size(); j++) {
                maxdiff = max(maxdiff, prices[j] - prices[i]);
            }
        }
        return maxdiff;
        */
        // Time out O(n^2)
        
        int minprice = INT_MAX;
        int maxprofit = 0;
        for (auto i : prices) {
            minprice = min(minprice, i);
            maxprofit = max(maxprofit, i - minprice);
        }
        return maxprofit;
    }
};
