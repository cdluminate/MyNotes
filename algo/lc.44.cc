#include <iostream>
#include <string>
#include <cassert>
using namespace std;

class Solution {
public:
    bool isMatch(string s, string p) {
        return isMatch((char*)s.c_str(), (char*)p.c_str());
    }
    bool isMatch(char* s, char* p) {
        if (*s == '\0' || *p == '\0') {
            return (*s == *p) || ((*p == '*') && (*s == '\0'));
        } else if (*p == *s) {
            return isMatch(++s, ++p);
        } else if (*p == '?') {
            return isMatch(++s, ++p);
        } else if (*p == '*') {
            while (*p == '*') p++; // skip repeated *
            if (*p == '\0') return true;
            while (*s != '\0' && !isMatch(s, p)) ++s;
            return *s != '\0';
        } else {
            return false;
        }
    }
}; // O(m!*n!) S(n)
// Note, * matches empty here.

int
main(void)
{
	auto s = Solution();
	cout << s.isMatch("", "?") << false << endl;
	cout << s.isMatch("", "*") << true << endl;
	cout << s.isMatch("a", "a*") << true << endl; // note this
	cout << s.isMatch("aa", "a*") << true << endl;
	cout << s.isMatch("aa","a") << false << endl;
	cout << s.isMatch("aa","aa") << true << endl;
	cout << s.isMatch("aaa","aa") << false << endl;
	cout << s.isMatch("aa", "*") << true << endl;
	cout << s.isMatch("ab", "?*") << true << endl;
	cout << s.isMatch("aab", "c*a*b") << false << endl;

	cout << s.isMatch("asd298fasd2", "a**2") << true << endl;
	return 0;
}
