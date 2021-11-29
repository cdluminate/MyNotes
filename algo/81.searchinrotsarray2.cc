class Solution {
public:
    bool search(vector<int>& nums, int target) {
        if (nums.empty()) return false;
        
        int curl = 0, curr = nums.size()-1;
        while (curl <= curr) {
            int curm = (curl + curr) / 2;
            if (nums[curm] == target) return true;
            
            if (nums[curl] < nums[curm]) { // left continuous
                if (nums[curl] <= target && target < nums[curm])
                    curr = curm - 1;
                else
                    curl = curm + 1;
            } else if (nums[curl] > nums[curm]) { // right continuous
                if (nums[curm] < target && target <= nums[curr])
                    curl = curm + 1;
                else
                    curr = curm - 1;
            } else { // can't decide which side is continuous, but n[curm] == n[curl]
                curl++;
            }
        }
        return false; // found nothing
    }
};
