#include <iostream>
#include <vector>
using namespace std;

#include "helper.hpp"

vector<int> nextperm(vector<int>& v) {
	if (v.empty()) return vector<int>{};

	// step1: R->L: first digit that violates the increasing trend
	int pivotidx = -1;
	for (int i = 0; i < (int)v.size()-1; i++) {
		if (v[i] < v[i+1]) {
			pivotidx = i;
		}
	}
	//cout << "pivotidx " << pivotidx << endl;
	// step1.1: if found no pivot point. The current sequence is
	// the largest permutation. Just reverse it and return.
	if (pivotidx < 0) {
		int curl = 0, curr = (int)v.size()-1;
		while (curl < curr) {
			int tmp = v[curl];
			v[curl] = v[curr];
			v[curr] = tmp;
			curl++; curr--;
		}
		return v;
	}
	// step2: R->L: first digit that is larget than partition number
	int changenum = 0;
	for (int i = 0; i < (int)v.size(); i++) {
		if (v[i] > v[pivotidx]) {
			changenum = i;
		}
	}
	//cout << "changenum " << changenum << endl;
	// step3: swap partition number and change number
	{
		int tmp = v[pivotidx];
		v[pivotidx] = v[changenum];
		v[changenum] = tmp;
	}
	//cout << "swapped " << endl;
	// step4: reverse the digits on the right side of partition index
	{
		int curl = pivotidx+1, curr = v.size()-1;
		while (curl < curr) {
			int tmp = v[curl];
			v[curl] = v[curr];
			v[curr] = tmp;
			curl++; curr--;
		}
	}
	//cout << "reversed" << v << endl;
	return v;
}

int
main(void)
{
	vector<int> a {1,2,3};
	vector<int> b {3,2,1};
	vector<int> c {1,1,5};
	vector<int> d {6, 8, 7, 4, 3, 2};

#define test(v) do { \
	cout << "Testing " << v << " -> " << nextperm(v) << endl; \
} while (0)

	test(a);
	test(b);
	test(c);
	test(d);

	vector<int> e {1,2,3,4};
	cout << e << endl;
	for (int i = 0; i < 30; i++) {
		e = nextperm(e);
		cout << e << endl;
	}

	return 0;
}
