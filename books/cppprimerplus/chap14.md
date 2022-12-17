Reusing code in C++
===

* the `valarray` class
```
#include <valarray>
valarray<int> values;
```

* private inheritance, with which public and protected members of the
base class become private members of the derived class.
```
class Student : private std::string, private std::valarray<double {
public:
  // containment constructor
  // Student(const char * str, const double * pd, int n) : name(str), scores(pd, n) {}
  // new constructor
  Student(const char * str, const double * pd, int n) : std::string(str), ArrayDb(pd, n) {}
  ...
};
```

* accessing base-class methods
```
double Student::Average() const {
  // original
  //if (scores.size() > 0) {
  //  return scores.sum()/scores.size();
  //} else {
  //  return 0;
  //}
  if (ArrayDb::size() > 0) {
    return ArrayDb::sum()/ArrayDb::size();
  } else {
    return 0;
  }
}
```

## Multiple Inheritance
...

## Class Templates
```
template <typename Tp>
class xxx {
  ...
};

template <typename Tp>
bool Stack<Tp>::push(const Tp & item) {
  ...
}

// using it
Stack<int> kernels;
```

* using a stack of pointers correctly  
...

* member templates  
...

* templates as parameters  
...

