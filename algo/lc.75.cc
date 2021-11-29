#include <vector>
#include <iostream>
using namespace std;

class Solution {
public:
    void sortColors(vector<int>& nums) {
        if (nums.empty()) return;
        
        // assume the input is valid
        int red = 0, white = 0, blue = 0; // 0 1 2
        // first pass: count
        for (auto i : nums) {
            if (i == 0) red++;
            else if (i == 1) white++;
            else if (i == 2) blue++;
        }
        // second pass: rewrite
        int wpos = 0;
		for (int i = 0; i < red; i++) nums[wpos++] = 0;
		for (int i = 0; i < white; i++) nums[wpos++] = 1;
		for (int i = 0; i < blue; i++) nums[wpos++] = 2;
    }
};

int
main(void)
{
	auto s = Solution();
	vector<int> x {0,2,1,2,1,1,0,0,2,1,1,1,0};
	s.sortColors(x);
	for (auto i : x) cout << " " << i;
	cout << endl;
	return 0;
}

