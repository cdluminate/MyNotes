/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    bool hasPathSum(TreeNode* root, int sum) {
        if (nullptr == root)
            return false;
        else if (!root->left && !root->right) {
            // leaf node
            return sum-root->val==0;
        } else {
            bool left = hasPathSum(root->left, sum-root->val);
            bool right = hasPathSum(root->right, sum-root->val);
            return left || right;
        }
    }
};
