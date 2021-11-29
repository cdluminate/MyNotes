class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        if (nums.empty()) return 0;
        int cur = 0;
        for (auto i : nums) {
            if (i != nums[cur]) {
                nums.at(++cur) = i;
            }
        }
        return cur+1;
    }
};
