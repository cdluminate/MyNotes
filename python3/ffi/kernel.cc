
#include <iostream>
#include <string>

int
kernel (char * s)
//kernel (std::string s)
{
  std::cout << s << std::endl;
  return 42;
}
