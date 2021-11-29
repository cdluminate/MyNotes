class Solution {
public:
    int singleNumber(vector<int>& nums) {
        vector<int> countbit(sizeof(int)*8, 0);
        // get the bit count
        for (auto i : nums) {
            for (int j = 0; j < sizeof(int)*8; j++) {
                countbit[j] += (i >> j) & 0x1;
                countbit[j] %= 3;
            }
        }
        // restore the single number
        int ret = 0;
        for (int j = 0; j < sizeof(int)*8; j++) {
            ret += (0x1 << j) * countbit[j];
        }
        return ret;
    }
};
