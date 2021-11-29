#include <iostream>
#include <vector>
#include "helper.hpp"
using namespace std;

class Solution {
public:
    void gameOfLife(vector<vector<int>>& board) {
        if (board.empty()) return;
        
        // Conv2d_same_3x3(in=board, kernel=[1], out=board), inplace modification
        int I = board.size();
        int J = board.front().size();
        for (int i = 0; i < I; i++) { for (int j = 0; j < J; j++) {
                // get out[i][j]
                int o = 0;
                for (int k : {-1, 0, 1}) { for (int l : {-1, 0, 1}) {
                    if (i+k < 0 || i+k>I-1) continue;
                    if (j+l < 0 || j+l>J-1) continue;
                    if (k == 0 && l == 0) continue;
                    o += board[i+k][j+l] % 10;
                } }
                board[i][j] += 10*o;
                //cout << board << endl;
        } }
        // state update
        for (int i = 0; i < I; i++) {
            for (int j = 0; j < J; j++) {
                int state    = board[i][j] % 10;
                int surround = board[i][j] / 10;
                if (state == 0) { // dead cell
                    board[i][j] = (surround == 3);
                } else { // live cell
                    board[i][j] = (surround == 2) || (surround == 3);
                }
            }
        }
        return;
    }
};

int
main(void)
{
    auto s = Solution();
    vector<vector<int>> board {
        vector<int>{0,0,0,0},
        vector<int>{0,1,1,0},
        vector<int>{0,1,1,0},
        vector<int>{0,0,0,0},
    };
    cout << board << endl;
    cout << "iter..." << endl;
    s.gameOfLife(board);    
    cout << board << endl;

    return 0;
}
