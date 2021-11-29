#include <iostream>
#include <cassert>

class Solution {
public:
  int getSum(int a, int b) {
    // imitate digital circuit
/* let's solve it with the K graph

 ci ai bi | o  cn
 0  0  0  | 0  0
 0  0  1  | 1  0
 0  1  0  | 1  0
 0  1  1  | 0  1
 1  0  0  | 1  0
 1  0  1  | 0  1
 1  1  0  | 0  1
 1  1  1  | 1  1

 o      = ai'bi'ci + ai'bici' + aibici + aibi'ci'
 c_next = aibi + aici + bici

 */
    using std::cout;
    using std::endl;

    int cn     = 0x0;
    int needle = 0x1;
    int ret    = 0x0;
    for (unsigned int i = 0; i < 8*sizeof(int); i++) {
cout << "iter" << i << " ";
      int ai = (a & needle);
      int bi = (b & needle);
      int ci = (cn & needle); // fetch c_prev and correct bit place
cout << "ai" << ai << " bi" << bi << " ci" << ci << " ";
      int output = needle&((~ai&~bi&ci) | (~ai&bi&~ci) | (ai&bi&ci) | (ai&~bi&~ci));
      cn  = (needle<<1)&(((ai&bi) | (ai&ci) | (bi&ci))<<1);
cout << " output" << output << " cn" << ci << " ";
      ret = ret | (output&needle);
cout << "update ret" << ret << " ";
      needle = needle << 1;
cout << "update needle" << needle << endl;
    }
    return ret;
  }
};

int
main (void)
{
  Solution s;
  assert(s.getSum(1, 2) == 3);
  assert(s.getSum(10, 20) == 30);
  assert(s.getSum(3, 3) == 6);
  assert(s.getSum(1234, 5678) == 6912);
  std::cout << "OK" << std::endl;
  return 0;
}
