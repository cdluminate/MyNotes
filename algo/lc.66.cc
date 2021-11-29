class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        int carry = 1;
        for (auto it = digits.rbegin(); it != digits.rend(); it++) {
            int x = *it + carry;
            *it = x % 10;
            carry = (int)x/10;
        }
        if (carry > 0)
            digits.insert(digits.begin(), carry);
        return digits;
    }
};
