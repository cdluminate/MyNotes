#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
public:
	int minMeetingRooms(vector<pair<int, int>>& intervals) {
		if (intervals.empty()) return 0;

		// get right bound. lbound = 0
		int rbound = 0;
		for (auto ij: intervals) {
			rbound = max(rbound, ij.first);
			rbound = max(rbound, ij.second);
		}
		// create counting vector
		vector<int> counts (rbound + 1, 0);
		// fill the vector
		for (auto ij : intervals) {
			for (int k = ij.first; k <= ij.second; k++) {
				counts[k]++;
			}
		}
		// find max val
		int minrooms = INT_MIN;
		for (auto i : counts) minrooms = max(minrooms, i);
		return minrooms;
	} // Naive solution
};

int
main(void)
{
	auto s = Solution();
	vector<pair<int,int>> intervals {
		pair<int,int>(0,30),
		pair<int,int>(5,10),
		pair<int,int>(15,20)
	};
	cout << s.minMeetingRooms(intervals) << endl;
	return 0;
}
