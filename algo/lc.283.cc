
#include <vector>
#include <iostream>

class Solution { 
public: 
    void moveZeroes(vector<int>& nums) { 
        unsigned int j = nums.size();
        for (unsigned int i = 0; i < j; i++) { 
            if (nums.at(i) != 0) { 
                continue; 
            } else { 
                int t = nums.at(i); 
                nums.erase(nums.begin()+i); 
                nums.push_back(t); 
                --i; --j;
            } 
        } 
    } 
};
