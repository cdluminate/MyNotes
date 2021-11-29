#include <iostream>
using namespace std;

class Solution {
public:
  int addDigits(int num) {
    int sum = 0;
    int n   = num;
    while (n != 0) {
      sum += n % 10;
      n = n / 10;
    }
    if (sum >= 10) return addDigits(sum);
    return sum;
  }
};

int
main (void)
{
  Solution s;
  cout << s.addDigits(38) << endl;
  return 0;
}
