class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int mask = 0;
        for (auto it = nums.begin(); it != nums.end(); it++) {
            mask ^= *it;
        }
        return mask;
    }
};
