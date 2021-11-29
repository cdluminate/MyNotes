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
    int minDepth(TreeNode* root) {
        if (nullptr == root) return 0;
        int mindepth = INT_MAX;
        helper(root, mindepth, 1);
        return mindepth;
    }
    void helper(TreeNode* root, int& mindepth, int curdepth) {
        if (nullptr == root) {
            return;
        } else if (root->left==nullptr && root->right==nullptr) {
            // leaf
            mindepth = (curdepth < mindepth) ? curdepth : mindepth;
        } else {
            // not leaf
            helper(root->left, mindepth, curdepth+1);
            helper(root->right, mindepth, curdepth+1);
        }
    }
};
