class Solution {
public:
    int trailingZeroes(int n) {
        /*
        int numzeros = 0;
        for (int i = 1; i <= n; i++) {
            int j = i;
            while (j % 5 == 0) {
                numzeros++;
                j /= 5;
            }
        }
        return numzeros;
        */ // time out
        return (n==0) ? 0 : (int)(n/5) + trailingZeroes(n/5);
    }
};
