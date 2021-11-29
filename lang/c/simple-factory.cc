
// -std=c++11

#include <iostream>
#include <string>
using namespace std;

///////////////////////////////////////////////////////////////

template <typename Tp>
class BiOperation {
protected: // using of private: here triggers error
  Tp nA_ = 0.;
  Tp nB_ = 0.;
public:
  Tp Aget (void) const { return nA_; }
  Tp Bget (void) const { return nB_; }
  Tp Aset (Tp n)       { nA_ = n; return nA_; }
  Tp Bset (Tp n)       { nB_ = n; return nB_; }
  virtual Tp GetResult (void) { return (Tp) 0.; }
  Tp GetResult (Tp A, Tp B) {
    nA_ = A; nB_ = B; return GetResult();
  }
}; // class biOperation

template <typename Tp>
class BiOperationAdd : public BiOperation<Tp> {
public:
  Tp GetResult (void) { return (Tp)(this->nA_ + this->nB_); }
}; // class BiOperationAdd

template <typename Tp>
class BiOperationSub : public BiOperation<Tp> {
public:
  Tp GetResult (void) { return (Tp)(this->nA_ - this->nB_); }
}; // class BiOperationSub

template <typename Tp>
class BiOperationMul : public BiOperation<Tp> {
public:
  Tp GetResult (void) { return (Tp)(this->nA_ * this->nB_); }
}; // class BiOperationMul

template <typename Tp>
class BiOperationDiv : public BiOperation<Tp> {
public:
  Tp GetResult (void) {
    if (this->nB_ == 0) throw "Bad denominator";
    return (Tp)(this->nA_ / this->nB_);
  }
}; // class BiOperationDiv

////////////////////////////////////////////////////////////////

template <typename Tp>
class BiOperationFactory {
public:
  BiOperation<Tp> * createOp (std::string oprt) {
    if (oprt == "+") {
      return new BiOperationAdd<Tp>();
    } else if (oprt == "-") {
      return new BiOperationSub<Tp>();
    } else if (oprt == "*") {
      return new BiOperationMul<Tp>();
    } else if (oprt == "/") {
      return new BiOperationDiv<Tp>();
    } else {
      throw "Invalid Operator!";
    }
  }
}; // class BiOperationFactory

////////////////////////////////////////////////////////////////

int
main (void)
{
  BiOperationFactory<double> * factory = new BiOperationFactory<double>;
  BiOperation<double> * op = NULL;
  {
    op = factory->createOp ("+");
    op->Aset (1.); op->Bset(2.);
    cout << op->GetResult() << endl;
  }
  {
    op = factory->createOp ("*");
    cout << op->GetResult(2, 3) << endl;
  }
  delete factory;
    
  return 0;
}
