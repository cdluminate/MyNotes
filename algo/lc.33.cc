class Solution {
public:
    int search(vector<int>& nums, int target) {
        if (nums.empty()) return -1;
        
        int curl = 0, curr = nums.size()-1;
        while (curl <= curr) {
            // invariant: target in curl..curr
            int curm = (curl + curr) / 2;
            if (nums[curm] == target) {
                return curm;
            } else if (nums[curl] <= nums[curm]) {
                // left side continuous
                if (nums[curl] <= target && target < nums[curm]) {
                    curr = curm-1;
                } else { // not here
                    curl = curm+1;
                }
            } else {
                // right side continuous
                if (nums[curm] < target && target <= nums[curr]) {
                    curl = curm+1;
                } else { // not here
                    curr = curm-1;
                }
            }
        }
        return -1; // found nothing
    }
};
