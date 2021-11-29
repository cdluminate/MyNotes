class Solution {
public:
    bool judgeCircle(string moves) {
        if (moves.empty()) return true;
        
        int curx = 0, cury = 0;
        for (char i : moves) {
            // move according to the instruction
            switch (i) {
                case 'R':
                    curx++; break;
                case 'L':
                    curx--; break;
                case 'U':
                    cury++; break;
                case 'D':
                    cury--; break;
                default:
                    // handle illegal input
                    continue;
            }
            // are we at the original point?
            //if (curx==0 && cury==0)
            //    return true;
        }
        return (curx==0 && cury==0);
    }
};
