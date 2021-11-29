#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

// leetcode 51 N-Queen
// DFS, O(n!*n) = O(4x3x2x1x isValid)

class Solution {
public:
    vector<vector<string>> solveNQueens(int n) {
		vector<vector<string>> results;
		vector<int> C(n, -1); // checkboard
		dfs(C, results, 0);
		return results;
    }
private:
	void dfs(vector<int>& C, vector<vector<string>>& results,
			 int row) {
		// boundary reached
		if ((int)C.size() == row) {
			vector<string> sol; // solution checkboard
			for (int i = 0; i < (int)C.size(); i++) {
				string line (C.size(), '.');
				line[C[i]] = 'Q';
				sol.push_back(line);
			}
			results.push_back(sol);
			return;
		}
		// not boundary
		for (int j = 0; j < (int)C.size(); j++) {
			// try every column
			bool avail = isValid(C, row, j);
			if (!avail) continue; // cut branch
			C[row] = j;
			dfs(C, results, row+1);
		}
	}
	bool isValid(const vector<int>& C, int row, int col) {
		// can we put a queen on location (row, col) of C?
		for (int i = 0; i < row; i++) {
			// this column has been occupied.
			if (C[i] == col) return false;
			// on the same diagonal
			// | x_c - x_q | = | y_c - y_q |
			if (abs(C[i]-col)==abs(i-row)) return false;
		}
		return true;
	}
};

int
main(void)
{
	auto s = Solution();
	auto results = s.solveNQueens(4);
	int count = 0;
	for (auto sol : results) {
		count++;
		cout << "-- Solution -- " << count << endl;
		for (auto line : sol) {
			for (char c : line) cout << " " << c;
			cout << endl;
		}
	}
	return 0;
}
