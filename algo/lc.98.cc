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
    bool isValidBST(TreeNode* root) {
        return isValidBST(root, nullptr, nullptr);
    }
    bool isValidBST(TreeNode* root, TreeNode* pmin, TreeNode* pmax) {
        if (nullptr == root) return true;
        if (pmin != nullptr && root->val <= pmin->val)
            return false;
        if (pmax != nullptr && root->val >= pmax->val)
            return false;
        return isValidBST(root->left, pmin, root) && isValidBST(root->right, root, pmax);
    }
};
