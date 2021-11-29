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
        if (*p == '\0') {
            return *s == *p; // * should match empty here
        } else if (*(p+1) != '*') { // without *
            if (!(*s == *p || (*p == '.' && *s != '\0'))) return false;
            return isMatch(s+1, p+1);
        } else { // with *
            if (isMatch(s, p+2)) return true;
            while (*s == *p || (*p == '.' && *s != '\0')) {
                if (isMatch(++s, p+2)) return true;
            }
        }
        return false;
    }
};

#define TEST(haystack, regex, groundtruth) do { \
    assert(s.isMatch(haystack, regex) == groundtruth); \
    cout << haystack << " / " << regex << " : OK" << endl; \
} while(0)

int
main(void)
{
    auto s = Solution();
    TEST("", "*", false);
    TEST("a", "a*", true);
    TEST("aa", "aa", true);
    TEST("aa", "a", false);
    TEST("aa", "a*", true);
    TEST("aa", "a.", true);
    TEST("aab", "c*a*b", true);
    TEST("aa", ".*", true);
    TEST("ab", ".*", true);
    TEST("aaa", "a*a", true);
	TEST("a", "ab*", true);
    return 0;
}
