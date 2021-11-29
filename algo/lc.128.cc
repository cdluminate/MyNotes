class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        if (nums.empty()) return 0;
        
        // create dict, O(n)
        map<int, bool> m;
        for (auto i : nums) m.insert(pair<int, bool>(i, false));
        
        // expand to both sides from each element
        int maxlen = 0;
        for (auto i : nums) {
            if (m[i] == true) continue;
            
            int curl = i, curu = i; // lower, upper
            map<int, bool>::iterator cur;
            
            // expand the lower bound
            while ((cur = m.find(curl)) != m.end()) {
                m[curl] = true;
                curl--;
            }
            // expand the upper bound
            while ((cur = m.find(curu)) != m.end()) {
                m[curu] = true;
                curu++;
            }
            // update maxlen
            maxlen = max(maxlen, curu-curl-1);
        }
        return maxlen;
    }
};
