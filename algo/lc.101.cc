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
    bool isSymmetric(TreeNode* root) {
        if (nullptr == root) return true;
        return helper(root->left, root->right);
    }
    bool helper(TreeNode* p, TreeNode* q) {
        if (nullptr == p && nullptr == q) return true;
        if (nullptr == p || nullptr == q) return false;
        return (p->val==q->val) &&
            helper(p->left, q->right) &&
            helper(p->right, q->left);
    }
};
