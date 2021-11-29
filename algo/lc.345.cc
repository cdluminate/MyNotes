#include <string>
#include <iostream>
using namespace std;

class Solution {
public:
  string reverseVowels(string s) {
    string ret = s;
    if (ret.size() == 0) return ret; // s = ""
    unsigned int l = 0; // left cursor
    unsigned int r = s.length()-1; // right cursor
    while (l < r) {
      //cout << l << r << endl;
      if (!isVowel(ret.at(l))) { ++l; continue; }
      if (!isVowel(ret.at(r))) { --r; continue; }
      char t = ret.at(l);
      ret.at(l) = ret.at(r);
      ret.at(r) = t;
      ++l; --r;
    }
    return ret;
  }

  bool isVowel(char s) const {
    switch (s) {
    case 'a':case 'e':case 'i':case 'o':case 'u':
    case 'A':case 'E':case 'I':case 'O':case 'U':
      return true;
    default:
      return false;
    }
    return false;
  }
};

int
main (void)
{
  Solution s;
  string msg1 = "hello";
  string msg2 = "leetcode";
  cout << s.reverseVowels(msg1) << endl;
  cout << s.reverseVowels(msg2) << endl;
  return 0;
}
