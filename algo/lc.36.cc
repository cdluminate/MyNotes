#include <vector>
#include <iostream>
using namespace std;

class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        vector<bool> dirty (9, false); // mask for [1, 9]

        // check lines
        for (int i = 0; i < 9; i++) {
            fill(dirty.begin(), dirty.end(), 0);
            for (int j = 0; j < 9; j++) {
                if (!check(board[i][j], dirty)) return false;
            }
        }
        // check rows
        for (int j = 0; j < 9; j++) {
            fill(dirty.begin(), dirty.end(), 0);
            for (int i = 0; i < 9; i++) {
                if (!check(board[i][j], dirty)) return false;
            }
        }
        // check blocks
        for (int bi = 0; bi < 3; bi++) {
            for (int bj = 0; bj < 3; bj++) {
                // check rows*lines of this block
                fill(dirty.begin(), dirty.end(), 0);
                for (int i = bi*3; i < bi*3+3; i++) {
                    for (int j = bj*3; j < bi*3+3; j++) {
                        if (!check(board[i][j], dirty))
                            return false;
                    }
                }
            }
        }
        // passed all checks
        return true;
    }
    bool check(char c, vector<bool> dirty) {
        if (c == '.') return true;
        if (dirty[c - '1']) {
			return false;
		} else {
			dirty[c - '1'] = true;
			return true;
		}
    }
};

int
main(void){
	std::vector<std::vector<char>> m {
		{'.','.','4', '.','.','.', '6','3','.'},
		{'.','.','.', '.','.','.', '.','.','.'},
		{'5','.','.', '.','.','.', '.','9','.'},

		{'.','.','.', '5','6','.', '.','.','.'},
		{'4','.','3', '.','.','.', '.','.','1'},
		{'.','.','.', '7','.','.', '.','.','.'},

		{'.','.','.', '5','.','.', '.','.','.'},
		{'.','.','.', '.','.','.', '.','.','.'},
		{'.','.','.', '.','.','.', '.','.','.'}
	}; // false??????
	
	auto s = Solution();
	cout << s.isValidSudoku(m) << endl;
	return 0;
}

// FIXME: wrong answer ???????????????
