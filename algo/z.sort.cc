/* 
 * @brief A collection of sorting algorithms.
 * Input : a vector of n numbers <a1, a2, ..., an>
 * Output: None, the given vector is sorted. Ascending.
 * @ref http://www.cnblogs.com/kkun/archive/2011/11/23/2260312.html
 */
#include <iostream>
#include <vector>
#include <algorithm>
#include "helper.hpp"
using namespace std;

namespace sort {

/* ----------------------------------------------- List of Sorting functions */

// kind: Selection, Selective Sort
// O(n^2), Unstable. suitable for small arrays.
template <typename DType> void selSort(vector<DType>&);

// kind: Selection, Naive Sort
// degradation of Selective sort.
template <typename DType> void naiveSort(vector<DType>&);

// kind: Selection
//void heapSort(vector<int>&);    

// kind: Swapping, Bubble Sort
// Stable.
template <typename DType> void bSort(vector<DType>&);

// kind: Swapping, Quick Sort
// O(n logn) @best. O(n^2) @worst. 
template <typename DType> void qSort(vector<DType>&);

// kind: Insertion
template <typename DType> void insSort(vector<DType>&);

// kind: Insertion
//void shellSort(vector<int>&);

// kind: Merge
template <typename DType> void mSort(vector<int>&);

// kind: Radix
//void radixSort(vector<int>&);

// kind: Bucket, Bucket Sort
// Stable. Very Fast. Memory Consuming. DType \in {Int, Long}
template <typename DType> void naiveBucketSort(vector<DType>&);

/* ------------------------------------------- END List of Sorting functions */

template <typename DType>
void
_mSort(vector<DType>& v, int curl, int curr) {
	if (curl >= curr) return; // len==0 or len==1
	else if (curl - curr == -1) { // len==2
		if (v[curl] > v[curr]) swap(v[curl], v[curr]);
	} else {
		_mSort(v, curl, (curl+curr)/2);
		_mSort(v, (curl+curr)/2+1, curr);
		// Merge two sorted arrays
		vector<DType> temp (curr - curl + 1, (DType)0.);
		int ml = curl, mr = (curl+curr)/2+1, mt = 0;
		while (ml <= (curl+curr)/2 && mr <= curr) {
			if (v[ml] < v[mr]) temp[mt++] = v[ml++];
			else temp[mt++] = v[mr++];
		}
		while (ml <= (curl+curr)/2) temp[mt++] = v[ml++];
		while (mr <= curr) temp[mt++] = v[mr++];
		//for (int i = 0; i < temp.size(); i++)
		//    v[curl+i] = temp[i];
		copy(temp.begin(), temp.end(), v.begin()+curl);
	}
}
template <typename DType>
void
mSort(vector<DType>& v) { return _mSort(v, 0, v.size()-1); }

template <typename DType>
void
naiveBucketSort(vector<DType>& v) {
	if (v.empty()) return;
	DType vmin = v[0], vmax = v[0];
	for (auto i : v) { vmin = min(vmin, i); vmax = max(vmax, i); }
	vector<int> bucket (vmax-vmin+1, 0);
	for (auto i : v) bucket[i-vmin]++;
	int cursor = 0;
	for (int i = 0; i < bucket.size(); i++)
		while (bucket[i]-- > 0) v[cursor++] = i + vmin;
}

template <typename DType>
void
bSort(vector<DType>& v) {
	for (int i = 0; i < v.size(); i++) {
		bool dirty = false;
		for (int j = v.size()-1; j > i; j--) {
			if (v[j] < v[j-1]) {
				dirty = true;
				swap(v[j], v[j-1]);
			}
		}
		if (!dirty) break;
	}
}

template <typename DType>
void
selSort(vector<DType>& v) {
    for (int i = 0; i < (int)v.size(); i++) {
        // find the mininum v_i for i in range [i, v.size)
        int idxmin = i;
        for (int j = i; j < (int)v.size(); j++) {
            idxmin = (v[j] < v[idxmin]) ? j : idxmin;
        }
        swap(v[i], v[idxmin]);
    }
}

template <typename DType>
void
naiveSort(vector<DType>& v) {
    for (int i = 0; i < v.size(); i++)
        for (int j = i; j < v.size(); j++)
            if (v[j] < v[i]) swap(v[j], v[i]);
}

template <typename DType>
void
_qSort(vector<DType>& v, int curl, int curr) {
	if (curl < curr) {
		int i = curl, j = curr;
		DType pivot = v[i];
		while (i < j) {
			while (i < j && v[j] > pivot) j--;
			if (i < j) v[i++] = v[j];
			while (i < j && v[i] < pivot) i++;
			if (i < j) v[j--] = v[i];
		}
		v[i] = pivot;
		_qSort(v, curl, i-1);
		_qSort(v, i+1, curr);
	}
}
template <typename DType>
void qSort(vector<DType>& v) { return _qSort(v, 0, v.size()-1); }

template <typename DType>
void
insSort (std::vector<DType>& v)
{
	if (v.empty()) return;
	for (int i = 0; i < v.size(); i++) { // i-1: sorted length 
		// find insert position, move v[i] to that position
		DType pivot = v[i];
		int j = i;
		while(j > 0 && pivot < v[j-1]) {
			v[j] = v[j-1];
			j--;
		}
		v[j] = pivot;
	}
	return;
}

} // namespace sort

#define _TEST(sortfun, i) do { \
	std::cout << "  :: Orig " << v##i << " -> Sorted "; \
	sortfun(v##i); std::cout << v##i << std::endl; \
} while(0)
#define TEST(name, sortfun) do { \
	std::cout << "=> Test " << name << std::endl; \
	std::vector<int> v1 {34,65,12,43,67,5,78,10,3,3,70}; \
	_TEST(sortfun, 1); \
	std::vector<int> v2 {123,12,11,5,7,43,7,4,7,467,1}; \
	_TEST(sortfun, 2); \
	std::vector<int> v3 {1,0,0,1,0,1,1,1,1,0,0,1,0}; \
	_TEST(sortfun, 3); \
	std::vector<int> v4 {100, 10}; \
	_TEST(sortfun, 4); \
	std::vector<int> v5 {}; \
	_TEST(sortfun, 5); \
} while(0)

int
main(void)
{
	TEST("Selective Sort", sort::selSort);
	TEST("Naive Sort", sort::naiveSort);
	TEST("Quick Sort", sort::qSort);
	TEST("Insertion Sort", sort::insSort);
	TEST("Bubble Sort", sort::bSort);
	TEST("Naive Bucket Sort", sort::naiveBucketSort);
	TEST("Merge Sort", sort::mSort);
    return 0;
}
