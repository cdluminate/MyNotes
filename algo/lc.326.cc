class Solution {
public:
    bool isPowerOfThree(int n) {
        /*
        if (n <= 0) return false;
        if (n == 1) return true;
        else if (n % 3 != 0) return false;
        else if (n / 3 == 1) return true;
        else return isPowerOfThree(n/3);
        */
        if (n <= 0) return false;
        return pow(3, (int)round(log(n)/log(3))) == n;
    }
};
