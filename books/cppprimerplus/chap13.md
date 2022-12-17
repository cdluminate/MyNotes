# Class inheritance

## Beginning with a simple base class

```
class Player {
private:
  ...
public:
  ...
};

class RatedPlayer : public Player {
...
};
```

a derived class needs its own constructors. a derived class can add
additional data menbers and member functions as needed.

```
RatedPlayer::RatedPlayer (unsigned int r, const string &fn,
    const string &ln, bool ht) : Player(fn, ln, ht) {
  rating = r;
}
```

* member initializer lists
```
derived::derived (type1 x, type2 y) : base(x,y) // initializer list
{ ... }
```

* relationship between derived and base classes
```
RatedPlayer rp1 (...);
Player * pp = & rp1;
Player & rp = rp1;
```

* polymorphic public inheritance: redefining base-class methods in a
derived class, using virtual methods. Keep in mind that although
nonvirtual functions are slightly more efficient than virtual
functions, they don't provide dynamic binding. Constructors can't be
virtual.

## Access control: `protected`

* abstract base classes
...

## Inheritance and Dynamic Memory Allocation
...

## Class design review
...
