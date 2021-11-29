class Solution {
public:
    string longestPalindrome(string s) {
        if (s.empty()) return 0;
        
        vector<vector<bool> > f(s.size(), vector<bool>(s.size(), false));
        int start = 0, maxlen=1;
        for (int j = 0; j < s.size(); j++) {
            f[j][j] = true;
            for (int i = 0; i < j; i++) {
                if (j==i) {
                    continue;
                } else if (j==i+1) {
                    f[i][j] = s[i]==s[j];
                } else { // j > i+1
                    f[i][j] = (s[i]==s[j]) && f[i+1][j-1];
                }
                
                if (f[i][j] && maxlen < (j-i+1)) {
                    maxlen = j-i+1;
                    start = i;
                }
            }
        }
        return s.substr(start, maxlen);
    }
};
