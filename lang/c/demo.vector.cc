#include <iostream>
#include <vector>

// http://www.cplusplus.com/reference/vector/vector

int
main(int argc, char** argv)
{
	std::vector<int> v;
	for (int i = 1; i < 11; i++)
		v.push_back(i);

	std::cout << "dump vector:";
	for (auto it = v.begin(); it != v.end(); it++) // auto:C++11
		std::cout << " " << *it;
	std::cout << std::endl;

	// XXX: Wrong
	//for (auto it = v.end(); it != v.begin(); it--)
	//	std::cout << " " << *it;
	//std::cout << std::endl;

	std::cout << "dump reversed vector:";
	for (auto it = v.rbegin(); it != v.rend(); it++)
		std::cout << " " << *it;
	std::cout << std::endl;

	std::cout << v.size() << std::endl;
	std::cout << v.empty() << std::endl;
	v.clear();
	std::cout << v.empty() << std::endl;


	return 0;
}
