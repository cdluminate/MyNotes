## Dynamic memory and classes

* static class members
```
class xxx {
private:
  const int p;
...
};

int xxx::p = 0; // initialize the static menber outsize please.
```

* special member functions
```
// in particular, c++ automatically provides the following member functions
// 1. default contructor
Klunk::Klunk() { } // implicit default constructor
Klunk::Klunk() { ... } // explicit default constructor
Klunk lunk; // invokes default constructor

// 2. default destructor
// 3. copy constructor, which does memberwise copying (shallow copying)
Class_name(const Class_name &);
StringBad ditto (motto); // calls StringBad(const StringBad &)
StringBad metoo = motoo; // calls StringBad(const StringBad &)
StringBad also = StringBad(motto); // calls StringBad(const StringBad &)
StringBad * p = new StringBad(motto); // calls StringBad(const StringBad &)
// for deep copying, define an explicit copy constructor

// 4. assignment operator
//    some times the default assignment operator suffers from the
//    shallow copy issue, fix it by explicit definition.

// 5. address operator
```

## When using `new` in constructors

If you use `new` in a constructor, you should also use `delete` in the
destructor.

```
NULL / 0 / nullptr
nullptr is from C++11
```

## Returnning Objects
...

## Using pointers to objects
...

## Reviewing Techniques

* overloading the `<<` operator
```
ostream & operator<<(ostream &os, const c_name &obj) {
  os << ...;
  return os;
}
```
