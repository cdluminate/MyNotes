BLAS
===

> blasqr.pdf , blas quick reference

```
Prefixes:
  x \in { S, D, C, Z }
  S - real, single precision
  D - double precision
  C - complex
  Z - complex * 16

Level2 and Level3:
  GE - GEneral
  TRANx - transpose
  UPLO  - upper triangular, lower triangular

```

## Level 1 BLAS
vector-vector operations.

A subroutine returns nothing.
```
subroutine xSWAP(N:dim,        X, INCX, Y, INCY)  # x <-> y
subroutine xSCAL(N:dim, alpha, X, INCX, Y, INCY)  # x <- ax
subroutine xCOPY(N:dim,        X, INCX, Y, INCY)  # y <- x
subroutine xAXPY(N:dim, alpha, X, INCX, Y, INCY)  # y <- ax+y
```

A function returns something.
```
function xDOT( N:dim, X, INCX, Y, INCY)            # ret <- x^T y
function xNRM2(N:dim, X, INCX         )            # ret <- ||x||_2
function xASUM(N:dim, X, INCX         )            # ret <- ||real(x)||_1 + ||imag(x)||_1
```

and so on.

## Level 2 BLAS
matrix-vector operations.

```
function xGEMV ( TRANS, M:dim, N:dim, alpha:scalar, A, LDA, X, INCX, BETA, Y, INCY )
 # y <- aAx + by   , A.size(m,n)
 # y <- aA^Tx + by , A.size(m,n)
 # y <- aA^Hx + by , A.size(m,n)

function xGER  (        M:dim, N:dim, alpha:scalar,         X, INCX,       Y, INCY, A, LDA)
 # A <- axy^T      , A.size(m,n)
```

and so on.

## Level 3 BLAS
matrix-matrix operations.

```
function xGEMM ( TRANSA, TRANSB, M:dim, N:dim, K:dim, alpha:scalar, A, LDA, B, LDB, BETA, C, LDC)
 # C <- a op(A) op(B) + bC,   op(X) \in X, X^T, X^H,    C.size(m,n)
```

and so on.

Nov 12. 2016
