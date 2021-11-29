class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        if (nums.size() <= 2) return nums.size();
        
        int idx = 2;
        for (int j = 2; j<nums.size(); j++) {
            if (nums[j] != nums[idx-2]) {
                nums[idx] = nums[j];
                idx++;
            }
        }
        return idx;
    }
};
