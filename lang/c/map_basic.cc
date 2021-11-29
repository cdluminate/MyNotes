/* http://www.cplusplus.com/reference/map/map/?kw=map */

#include <iostream>
#include <map>
#include <string>
using namespace std;

int
main(void)
{
  // construct
  map<int, string> m;

  // adding key and value pairs
  m.insert(pair<int, string>(1, "hello"));
  m.insert(map<int, string>::value_type(2, "world"));
  m[3] = "!";
  m[5] = "\n";
  
  // search
  map<int, string>::iterator cursor;
  cursor = m.find(4);
  if (cursor == m.end()) cout << "key 4 not found" << endl;
  cursor = m.find(5);
  if (!(cursor == m.end())) cout << "key 5 found" << endl;

  // delete
  m.erase(cursor); // erase 5

  return 0;
}
