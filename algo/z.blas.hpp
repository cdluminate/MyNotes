/**
 * @file z.blas.hpp
 * @brief Naive BLAS
 */
#if ! defined(Z_BLAS_HPP_)
#define Z_BLAS_HPP_

#include <algorithm>
#include <cassert>
#include <cmath>
#include <iostream>
#include <vector>

/* 1D vector dump */
template <typename T>
std::ostream&
operator<< (std::ostream& out, const std::vector<T>& v) {
	if (v.empty()) {
		out << "[]";
	} else {
		out << "[";
		for (auto i : v) out << i << ", ";
		out << "\b\b]";
	}
	return out;
}

/* 2D vector (matrix) dump */
template <typename T>
std::ostream&
operator<< (std::ostream& out,
		const std::vector<std::vector<T>>& m) {
	out << "[" << std::endl;
	for (auto v : m) {
		out << "  " << v;
	}
	out << "]" << std::endl;
	return out;
}

namespace tensor { //                                                    TENSOR
/* vector and matrix generator */

} // namespace tensor                                                    TENSOR

namespace blas { //                                                        BLAS
/*
https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms
http://www.netlib.org/blas/
*/

/* LEVEL1: amax : amax = max|x_i| */
template <typename DType>
DType
amax(std::vector<DType>& x)
{
	DType absmax = (DType)0.;
	for (auto xi : x) {
		DType absxi = (xi > (DType)0.) ? xi : -xi;
		absmax      = (xi > absmax)    ? xi : absmax;
	}
	return absmax;
}

/* LEVEL1: asum : asum <- ||x||_1 */
/* vector absolute sum, asum = \sum_i abs(x_i) */
template <typename DType>
DType
asum (std::vector<DType>& v)
{
	DType ret = (DType)0.;
	for (auto vi : v) ret += (vi>0) ? vi : -vi;
	return ret;
}

/* LEVEL1: axpy : y <- ax + y*/
template <typename DType>
void
axpy(DType alpha,
     std::vector<DType>& x,
     std::vector<DType>& y)
{
	assert(x.size() == y.size());
	for (int i = 0; i < x.size(); i++) y[i] += alpha * x[i];
}

/* LEVEL1 EXTRA: axpby : y <- ax + by */
template <typename DType>
void
abpby(DType alpha,
      std::vector<DType>& x,
      DType beta,
      std::vector<DType>& y)
{
	assert(x.size() == y.size());
	for (int i = 0; i < x.size(); i++) y[i] = alpha * x[i] + beta * y[i];
}

/* LEVEL1: copy : y <- x */
template <typename DType>
void
copy(std::vector<DType>& x,
     std::vector<DType>& y)
{
	assert(x.size() == y.size());
	copy(x.begin(), x.end(), y.begin());
}

/* LEVEL1: dot  : dot <- x^T y */
template <typename DType>
DType
dot(std::vector<DType> x,
     std::vector<DType> y)
{
	assert(x.size() != y.size());
	DType ret = (DType) 0.;
	for (int i = 0; i < (int)x.size(); i++) ret += x[i] * y[i];
	return ret;
}

/* LEVEL2: nrm2 : nrm2 <- ||x||_2 */
template <typename DType>
DType
nrm2(std::vector<DType>& x)
{
	DType ret = (DType)0.;
	for (auto xi : x) ret += xi * xi;
	return sqrt(ret);
}

/* LEVEL1: scal : x <- ax */
template <typename DType>
void
scal(DType alpha,
     std::vector<DType>& x)
{
	for (int i = 0; i < x.size(); i++) x[i] *= alpha;
}

/* LEVEL1 EXTRA: sum = sum_i x_i */
template <typename DType>
DType
sum(std::vector<DType>& x)
{
	DType sum = (DType)0.;
	for (auto xi : x) sum += (DType)xi;
	return sum;
}

/* LEVEL1 EXTRA: mean = sum(x)/len(x) */
template <typename DType>
DType
mean(std::vector<DType>& v)
{
	return sum(v)/v.size();
}

/* LEVEL1: swap : x <-> y */
template <typename DType>
void
swap(std::vector<DType>& x,
     std::vector<DType>& y)
{
	std::vector<DType> tmp (x);
	copy(y, x);
	copy(tmp, y);
}

/* LEVEL2: gemv : y <- aAx + by */
template <typename DType>
void
gemv(DType alpha,
     std::vector<std::vector<DType>>& A,
     std::vector<DType>& x,
     DType beta,
     std::vector<DType>& y)
{
	// size(A) = (M, N), size(x) = (N, 1), size(y) = (M, 1)
	int M = A.size(); // N = x.size();
	for (int m = 0; m < M; m++) {
		y[m] = alpha * dot(A[m], x) + beta * y[m];
	}
}

/* LEVEL3: gemm : C <- aAB + bC */
template <typename DType>
void
gemm(DType alpha,
     std::vector<std::vector<DType>>& A,
     std::vector<std::vector<DType>>& B,
     DType beta,
     std::vector<std::vector<DType>>& C)
{
	// size(A)=(M,K), size(B)=(K,N), size(C)=(M,N)
	int M = C.size(), N = C.front().size(), K = A.front().size();
	for (int m = 0; m < M; m++) {
		for (int n = 0; n < N; n++) {
			C[m][n] *= beta;
			for (int k = 0; k < K; k++) {
				C[m][n] += alpha * A[m][k] * B[k][n];
			}
		}
	}
}

} // namespace blas                                                        BLAS

#endif // Z_BLAS_HPP_
