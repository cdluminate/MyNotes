Friends, Exceptions
===

* friends
```
classs TV {
private:
  int state, volume, maxchannel, mode, input;
public:
  friend class Remote; // remote can access private part of TV.
  TV(int s = Off, int mc = 125) : state(s), volume(5),
    maxchannel(mc), channel(2), mode(Cable), input(TV) {}
  ...
};

class Remote {
private:
  int mode; // controls TV or DVD
public:
  Remote(int m = TV::Tv) : mode(m) {}
  ...
}; 
```

* nested classes
```
class Team
{
public:
class Coach { ... };
...
};
```

* Exceptions
```
#include <cstdlib>
void abort(void);
```

try-catch
```
double x, z;
while (std::cin >> x) {
  try {
    z = test(x);
  } catch (const char * s) {
    std::cout << s << std::endl;
    continue;
  }
}
double test (double x) {
  if (x == 0.) {
    throw "0 is not allowed"; 
  }
  return x;
}
```

* Run-time Type Identification (RTTI)

`dynamic_cast` operator
```
// if this pointer type is not safe, pm will recieve NULL
Superb * pm = dynamic_cast<Superb *> (pg);
// general form
dynamic_cast<Type *> (pt)
```

`typeid` operator
```
TODO
```

`static_cast` operator

`const_cast` operator

`reinterpret_cast` operator

