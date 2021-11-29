#include <vector>
#include <iostream>
#include <map>

using namespace std;
#include "helper.hpp"

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // assume that input is valid
        map<int, int> m;
        map<int, int>::iterator cur;
        for (int i = 0; i < (int)nums.size(); i++) {
            if ((cur = m.find(target-nums[i])) != m.end())
                return vector<int> {i, cur->second};
			m.insert(pair<int,int>(nums[i], i));
        }
        return vector<int>{-1, -1};
    }
};

int
main(void)
{
	auto s = Solution();
	vector<int> v {3, 2, 4};
	cout << s.twoSum(v, 6) << endl;
	return 0;
}
