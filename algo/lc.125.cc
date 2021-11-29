class Solution {
public:
    bool isPalindrome(string s) {
        if (0 == s.size())
            return true;
        for (int i = 0; i < s.size(); i++) {
            s[i] = tolower(s[i]);
        }
        int curl = 0, curr = s.size()-1;
        while (curl < curr) {
            if (!isalpha(s[curl]) && !isdigit(s[curl])) {
                curl++;
            } else if (!isalpha(s[curr]) && !isdigit(s[curr])) {
                curr--;
            } else if (s[curl] != s[curr]) {
                return false;
            } else { // s[curl] == s[curr]
                curl++; curr--;
            }
        }
        return true;
    }
};
