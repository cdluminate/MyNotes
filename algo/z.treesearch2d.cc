#include <iostream>
#include <vector>
using namespace std;

#include "helper.hpp"

void treeSearch2D(vector<vector<int>>&, int, int);
int pcount = 0; // print count
void dumpMat(const vector<vector<int>>&);

int
main(void)
{
	// mat = zeros(2, 3)
	vector<vector<int>> mat;
	for (int i = 0; i < 2; i++) mat.push_back(vector<int>(3, 0));
	// do search
	treeSearch2D(mat, 0, 0);
	cout << "dump pcount " << pcount << endl; // 2**6 = 64

	pcount = 0;
	// tril = [[0], [0,0], [0,0,0]]
	vector<vector<int>> tril;
	tril.push_back(vector<int>(1, 0));
	tril.push_back(vector<int>(2, 0));
	tril.push_back(vector<int>(3, 0));
	// do search
	treeSearch2D(tril, 0, 0);
	cout << "dump pcount " << pcount << endl; // 2**6 = 64

	return 0;
}

void dumpMat(const vector<vector<int>>& mat, bool flatten) {
	for (int i = 0; i < (int)mat.size(); i++) {
		cout << " ";
		for (int j = 0; j < (int)mat[i].size(); j++) {
			cout << " " << mat[i][j];
		}
		if (!flatten) cout << endl;
	}
	if (flatten) cout << endl;
}

void treeSearch2D(vector<vector<int>>& mat, int curr, int curc) {
	//cout << "* searching -> " << curr << ", " << curc << endl;
	// row boundary reached, col ANY
	if ((int)mat.size() == curr) {
		pcount++;
		cout << " -- dump -- " << pcount << endl;
		//dumpMat(mat, true);
		std::cout << mat;
		return;
	}
	// row ANY, col boundary reached
	if (curc == (int)mat[curr].size()-1) {
		for (int i = 0; i < 2; i++) {
			mat[curr][curc] = i;
			treeSearch2D(mat, curr+1, 0);
		}
		return;
	}
	// row ANY, col boundary not reached
	if (curc < (int)mat[curr].size()) {
		for (int i = 0; i < 2; i++) {
			mat[curr][curc] = i;
			treeSearch2D(mat, curr, curc+1);
		}
		return;
	}
}
