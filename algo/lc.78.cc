class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int> > res;
        vector<int> buf(nums.size(), 0);
        em(buf, 0, nums, res);
        return res;
    }
    void em(vector<int>& buf, int cur, vector<int>& nums, vector<vector<int> >& res) {
        if (cur == buf.size()) {
            vector<int> v;
            for (int i = 0; i < buf.size(); i++) {
                if (buf[i] == 1) v.push_back(nums[i]);
            }
            res.push_back(v);
            return;
        } else {
            for (int i = 0; i < 2; i++) {
                buf[cur] = i;
                em(buf, cur+1, nums, res);
            }
        }
    }
};
