Lapack note
===

> lapackqref.ps, LAPACK quich reference guide to the driver routines  
> http://docs.oracle.com/cd/E19059-01/fortec6u2/806-7993/sgesv.html  
> http://docs.oracle.com/cd/E19059-01/fortec6u2/806-7993/sgels.html  

```
x \in S,D,C,Z
```

# simple drivers

## linear equations
```
xGESV( N, NRHS, A, LDA, IPIV, B, LDB, INFO ) # solve A*X=B
 * N (input) The number of linear equations, i.e., the order of the matrix A. N >= 0.
 * NRHS (input) The number of right hand sides, i.e., the number of columns of the matrix B. NRHS >= 0.
 * A (input/output) On entry, the N-by-N coefficient matrix A. On exit, the factors L and U from the factorization A = P*L*U; the unit diagonal elements of L are not stored.
 * LDA (input) The leading dimension of the array A. LDA >= max(1,N).
 * IPIVOT (output) The pivot indices that define the permutation matrix P; row i of the matrix was interchanged with row IPIVOT(i).
 * B (input/output) On entry, the N-by-NRHS matrix of right hand side matrix B. On exit, if INFO = 0, the N-by-NRHS solution matrix X.
* LDB (input) The leading dimension of the array B. LDB >= max(1,N).
* INFO (output) 
```

## standard and generalized linear least squares problems
```
xGELS( TRANS, H, N, NHRS, A, LDA, B, LDB, WORK, LWORK, INFO )

sgels - solve overdetermined or underdetermined real linear systems involving an M-by-N matrix A, or its transpose, using a QR or LQ factorization of A
```

TODO

# expert drives

TODO
