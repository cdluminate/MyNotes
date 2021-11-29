class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        if (nums.empty()) return 0;
        
        int cursor = 0;
        while (cursor < nums.size() && nums[cursor] <= target) {
            if (nums[cursor] == target) return cursor;
            cursor++;
        }
        return cursor;
    }
};
