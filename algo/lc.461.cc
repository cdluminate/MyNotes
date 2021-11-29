class Solution {
public:
    int hammingDistance(int x, int y) {
        int numofbit1 = 0;
        int d = x^y;
        for (int i = 0; i < 32; i++) {
            numofbit1 += (d >> i) & 0x1;
        }
        return numofbit1;
    }
};
