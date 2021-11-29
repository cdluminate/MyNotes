#include <iostream>
#include <vector>
#include <stack>
#include "helper.hpp"

using namespace std;
int pcount = 0; // print count

void
treeSearch(std::vector<int>& buf, int cur) {
	if (cur == (int)buf.size()) {
		std::cout << buf << std::endl;
		pcount++;
	} else {
		for (int i = 0; i < 2; i++) {
			buf[cur] = i;
			treeSearch(buf, cur+1);
		}
	}
}

void
treeSearchByStack(int len, std::vector<int>& v)
{
	if (len == v.size()) { // boundary
		cout << v << endl;
		pcount++;
	} else { // enter into next bit
		for (int i = 0; i < 2; i++) {
			v.push_back(i);
			treeSearchByStack(len, v);
			(void) v.pop_back();
		}
	}
}

int
main(void)
{
	std::vector<int> v(3, 0);

	pcount = 0;
	treeSearch(v, 0);
	std::cout << "treeSearch pcount " << pcount << std::endl;

	v.clear();
	pcount = 0;
	treeSearchByStack(3, v);
	std::cout << "treeSearchByStack pcount " << pcount << std::endl;

	return 0;
}
