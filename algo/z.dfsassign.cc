/**
 * @file assign.cc
 * @brief solve task assigning problem
 */
#include <vector>
#include <iostream>
#include <climits>
#include "helper.hpp"
using namespace std;

bool
seqSearch (std::vector<int>& v, int target) {
	for (unsigned int j = 0; j < v.size(); j++)
		if (v[j] == target) return true;
	return false;
}

void
bestperm (int cost [4][4], std::vector<int>& buf,
	std::vector<int>& solution, int& solution_sum)
{
	if (buf.size() == 4) { // boundary
		int cur_sum = 0;
		for (unsigned int i = 0; i < 4; i++) {
			cur_sum += cost[i][buf.at(i)];
		}
		if (cur_sum < solution_sum) {
			solution_sum = cur_sum;
			solution = buf;
		}
	} else { // non-boundary
		for (unsigned int i = 0; i < 4; i++) {
			if (seqSearch(buf, i)) continue;
			else {
				buf.push_back(i);
				bestperm(cost, buf, solution, solution_sum);
				(void) buf.pop_back();
			}
		}
	}
	return;
}

int
main (void)
{
	int cost[4][4] = {
		{9,2,7,8},
		{6,4,3,7},
		{5,8,1,8},
		{7,6,9,4}
	};
	std::vector<int> solution;
	std::vector<int> buffer;
	int solution_sum = INT_MAX;
	bestperm(cost, buffer, solution, solution_sum);
	cout << "dump solution";
	xvdump(solution);
	cout << " with total cost " << solution_sum << endl;

	return 0;
}
