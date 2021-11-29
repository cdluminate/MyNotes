#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        /*
        // assume nums is not empty
        map<int, bool> m;
        map<int, bool>::iterator cur;
        for (auto i : nums) {
            if ((cur = m.find(i)) != m.end()) {
                // found
                return i;
            } else {
                // not found
                m[i] = true;
            }
        }
        // no duplicate ??
        return 0; // O(n) S(n)
        */
        
        // assume that input is valid. the list contains a ring.
        // at the node they meet:
        //   cur1 = x + a
        //   cur2 = x + a + n*r
        //   => x = n*r - a
        //   where x = [head,entrance), a = [entrance, meet),
        //   r = [entrance, entrance)
        
        
        // init
        int cur1 = nums[0];
        int cur2 = nums[nums[0]];
        
        // find the point at which they meet
        while (cur1 != cur2) {
            cur1 = nums[cur1];
            cur2 = nums[nums[cur2]];
        }
        
        // reset the fast cursor
        cur2 = 0;
        
        // find the entrance
        while (cur1 != cur2) {
            cur1 = nums[cur1];
            cur2 = nums[cur2];
        }
        
        return cur1; // O(n) S(1)
    }
};

int
main(void)
{
	vector<int> v {1,2,3,3,4};
	auto s = Solution();
	cout << s.findDuplicate(v) << endl;
	return 0;
}
