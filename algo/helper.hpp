/**
 * @file helper.hpp
 * @brief misc helper functions including printing, etc.
 */
#if ! defined(HELPER_HPP_)
#define HELPER_HPP_

#include <iostream>
#include <vector>
#include <cassert>
#include <cmath>

//https://stackoverflow.com/questions/10750057/how-o-print-out-the-contents-of-a-vector

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

/* old dumping function */
template <typename DType>
void
xvdump (std::vector<DType> buf)
{
	using namespace std;
	for (unsigned int i = 0; i < buf.size(); i++)
		cout << buf[i] << " ";
	cout << endl;
	return;
}

/* x-typed vector absolute sum, b = \sum_i abs(a_i) */
template <typename DType>
DType
xvasum (std::vector<DType> bottom)
{
	DType ret = (DType)0;
	for (unsigned int i = 0; i < bottom.size(); i++) {
		int j = bottom[i];
		ret += (j>0) ? j : -j;
	}
	return ret;
}

/* x-typed vector dot product, c = \sum_i a_i * b_i */
template <typename DType>
DType
xvdot (std::vector<DType> x, std::vector<DType> y)
{
	DType ret = (DType) 0.;
	if (x.size() != y.size()) {
		std::cout << "E: vector_dot: vector size mismatch!" << std::endl;
	} else {
		for (unsigned int i = 0; i < x.size(); i++)
			ret += x[i] * y[i];
	}
	return ret;
}

double
xamean(int *v, size_t sz) {
	double sum = .0;
	for (int i = 0; i < sz; i++) {
		sum += (double)(v[i]);
	}
	return sum/sz;
}

// temperature convertion: F -> C
float
tempconv(float f)
{
	return 5.*(f-32.)/9.;
}

long
sum1ton(int n)
{
	long sum = 0;
	for (int i = 1; i <= n; i++)
		sum += i;
	return sum;
}

#define PI (( 4.*atan(1.0) ))
float sinfa(float n) { return sinf(n*PI/180.); }
float cosfa(float n) { return cosf(n*PI/180.); }

// number of digits
int
getNumDigits(int n) {
	int counter = 0;
	while (n > 0) {
		n /= 10;
		counter ++;
	}
	return counter;
}

#endif // HELPER_HPP_
