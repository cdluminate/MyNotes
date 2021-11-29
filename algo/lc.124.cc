/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */

#include <climits>
#include <iostream>

#define max(a, b) ((a>b) ? a : b)

struct TreeNode {
	int val;
	TreeNode* left;
	TreeNode* right;
	TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    int maxPathSum(TreeNode* root) {
        if (root == nullptr) return 0;
        int maxpathsum = INT_MIN;
        helper(root, &maxpathsum);
        return maxpathsum;
    }
    int helper(TreeNode* root, int* maxpathsum) {
        if (nullptr == root) return 0;
        else {
            int left = max(0, helper(root->left, maxpathsum));
            int right = max(0, helper(root->right, maxpathsum));
            *maxpathsum = max(*maxpathsum, left+right+root->val);
			//std::cout << left << " " << right << " " << *maxpathsum << std::endl;
            return max(left, right) + root->val;
        }
    }
};

int
main(void)
{
	auto s = Solution();
	auto a = TreeNode(1);
	auto b = TreeNode(2);
	auto c = TreeNode(3);
	b.left = &a; b.right = &c;

	std::cout << s.maxPathSum(&b);

	return 0;
}
