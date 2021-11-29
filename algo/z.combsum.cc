#include <iostream>
#include <vector>
#include "helper.hpp"
using namespace std;

// note the difference between leetcode #39.

class Solution {
public:
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        vector<vector<int>> solutions;
        vector<int> combmask (candidates.size(), 0);
        helper(solutions, candidates, combmask, target, 0);
        return solutions;
    }
    int vdot(vector<int> a, vector<int> b) {
        // a^T b, len(a)==len(b)
        int ret = 0;
        for (int i = 0; i < a.size(); i++) {
            ret += a[i]*b[i];
        }
        return ret;
    }
    vector<int> getComb(vector<int>& v, vector<int>& combmask) {
        vector<int> ret;
        for (int i = 0; i < v.size(); i++) {
            if (combmask[i] > 0) ret.push_back(v[i]);
        }
        return ret;
    }
    void helper(vector<vector<int>>& solutions, vector<int>& candidates,
                vector<int>& combmask, int target, int cursor) {
        if (cursor == candidates.size()) {
			cout << combmask << " " << vdot(combmask, candidates) << endl;
            // boundary
            if (vdot(combmask, candidates) == target)
                solutions.push_back(getComb(candidates, combmask));
        } else {
            // non-boundary
            for (int i = 0; i < 2; i++) {
                combmask[cursor] = i;
                helper(solutions, candidates, combmask, target, cursor+1);
            }
        }
    }
};

int
main(void)
{
	auto s = Solution();
	vector<int> candidates {2,3,6,7,4};
	cout << "Orig " << candidates << endl;
	cout << s.combinationSum(candidates, 7) << endl;

	return 0;
}
