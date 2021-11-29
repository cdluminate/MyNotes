#include <iostream>
#include <functional>

// https://msdn.microsoft.com/zh-cn/library/dd293608.aspx

int
main(void)
{
	auto lambda = [](auto a, auto b) { return a+b; };
	std::cout << lambda(1,2) << std::endl;
	std::cout << lambda(3.5, 4.5) << std::endl;

	std::function<long(int)> factorial = [&](int n) {
		return (n==1) ? 1 : n*factorial(n-1);
	};
	std::cout << factorial(5) << std::endl;
	return 0;
}
