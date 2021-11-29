#include <iostream>
#include <vector>
#include "helper.hpp"
using namespace std;

bool bisearch_iter(vector<int>& v, int target)
{
	// empty vector
	if (v.empty()) return false;

	int curl = 0, curr = v.size() - 1;
	while (curl <= curr) {
		// invariant: target in v[curl]..v[curr]
		int curm = (curl + curr) / 2;
		if (v[curm] == target) {
			return true;
		} else if (v[curm] > target) {
			curr = curm-1;
		} else { // v[curm] < target
			curl = curm+1;
		}
	}
	return false;
}

bool bisearch_recu_(vector<int>& v, int target, int curl, int curr)
{
	// not empty
	if (v.empty()) return false;
	// invariant: target in v[curl]..v[curr]
	
	// boundary
	if (curl == curr) {
		return v[curl] == target;
	}
	// not boundary
	int curm = (curl + curr) / 2;
	if (v[curm] == target) {
		return true;
	} else if (v[curm] > target) {
		return bisearch_recu_(v, target, curl, curm-1);
	} else { // v[curm] < target
		return bisearch_recu_(v, target, curm+1, curr);
	}
}
bool bisearch_recu(vector<int>& v, int target) {
	return bisearch_recu_(v, target, 0, v.size()-1);
}

/**
 * @brief sequential search
 */
template <typename DType>
int
sequentialSearch(const std::vector<DType>& v, DType target)
{
	for (int i = 0; i < v.size(); i++)
		if (v[i] == target) return i;
	return -1;
}

int
main(void)
{
	{
	vector<int> v {1,2,3,4,5,6,7,8,9,10};
	cout << bisearch_iter(v, -1) << bisearch_recu(v,-1) << endl;
	cout << bisearch_iter(v, 1)  << bisearch_recu(v,1)  << endl;
	cout << bisearch_iter(v, 2)  << bisearch_recu(v,2)  << endl;
	cout << bisearch_iter(v, 6)  << bisearch_recu(v,6)  << endl;
	cout << bisearch_iter(v, 10) << bisearch_recu(v,10) << endl;
	cout << bisearch_iter(v, 11) << bisearch_recu(v,11) << endl;
	}

	{
	//int i;
	//while (std::cin >> i) buf.push_back(i);
	std::vector<int> buf {1,2,3,4,5,6,7,8,9};
	std::cout << sequentialSearch(buf, 5) << std::endl;
	std::cout << sequentialSearch(buf, 10) << std::endl;
	}
	return 0;
}
