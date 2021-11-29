#include <iostream>
using std::cout;
using std::endl;

class Solution {
public:
  bool canWinNim(int n) {
/*
  n = 1 -> win
  n = 2 -> win
  n = 3 -> win
  n = 4 -> loss no matter how many stones you remove
  n = 5 -> you remove 1, win. (leaving 4 to the other side)
  n = 6 -> you remove 2, win. (leaving 4 to the other side)
  n = 7 -> you remove 3, win. (leaving 4 to the other side)
  n = 8 -> loss no matter how many stones you remove
  ...
  n = (4 * k) + m, k in Z, m in { 1 2 3 } -> win
  n = (4 * k), k in Z -> lose
 */
    return (n % 4 != 0);
  }
};

int
main (void)
{
  Solution s;
  cout << s.canWinNim(1);
  cout << s.canWinNim(2);
  cout << s.canWinNim(3);
  cout << s.canWinNim(4);
  cout << endl;
  return 0;
}
