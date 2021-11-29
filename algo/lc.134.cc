class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        
        int sumdiff = 0;
        // enough gas?
        for (int i = 0; i < gas.size(); i++)
            sumdiff += gas[i] - cost[i];
        if (sumdiff < 0)
            return -1;
        
        // gas enough.
        int sumseg = 0;
        int mark = -1;
        for (int i = 0; i < gas.size(); i++) {
            sumseg += gas[i] - cost[i];
            if (sumseg < 0) {
                mark = i;
                sumseg = 0;
            }
        }
        return mark+1;
    }
};
