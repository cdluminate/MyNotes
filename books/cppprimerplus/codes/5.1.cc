#include <iostream>
using namespace std;

int
main (void)
{
  // C++11 new feature: 
  // range-based loop
  for (int x: { 1, 2, 3, 4, 5 }) {
    cout << x << endl;
  }
  return 0;
}
