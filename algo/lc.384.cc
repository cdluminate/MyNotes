#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include "helper.hpp"
using namespace std;

// reference: CPython/Lib/random.py :: random.shuffle()

class Solution {
public:
    vector<int> origin;
    vector<int> shuffled;
    
    Solution(vector<int> nums) {
		origin = nums;
		shuffled = nums;
    }
    
    /** Resets the array to its original configuration and return it. */
    vector<int> reset() {
        return origin;
    }
    
    /** Returns a random shuffling of the array. */
    vector<int> shuffle() {
        for (int i = shuffled.size()-1; i >= 0; i--) {
            int j = rand() % (i + 1); // j=randint([0,i])
            swap(shuffled[i], shuffled[j]);
        }
        return shuffled;
    }
};

/**
 * Your Solution object will be instantiated and called as such:
 * Solution obj = new Solution(nums);
 * vector<int> param_1 = obj.reset();
 * vector<int> param_2 = obj.shuffle();
 */

int
main(void)
{
	srand(1);
	vector<int> v {1,2,3,4,5,6,7,8};
	auto s = Solution(v);
	cout << "Orig " << v << endl;
	cout << "Shuf " << s.shuffle() << endl;
	cout << "Shuf " << s.shuffle() << endl;
	cout << "Shuf " << s.shuffle() << endl;
	srand(100);
	cout << "Shuf " << s.shuffle() << endl;
	cout << "Shuf " << s.shuffle() << endl;
	cout << "Shuf " << s.shuffle() << endl;
	cout << ":orig" << s.reset() << endl;
	return 0;
}
