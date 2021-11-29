class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        if (nums.empty()) return 1;
        
        map<int, bool> m;
        int n_max = INT_MIN;
        for (int i : nums) { // O(n) S(n)
            m[i] = true;
            n_max = max(n_max, i);
        }
        
        for (int i = 1; i <= n_max; i++) { // O(constant)
            map<int, bool>::iterator cur = m.find(i);
            if (cur == m.end()) {
                // not found
                return i;
            }
        }
        return n_max+1;
    }
};
