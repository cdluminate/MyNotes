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
    vector<int> postorderTraversal(TreeNode* root) {
        vector<int> traj;
        helper(root, traj);
        return traj;
    }
    void helper(TreeNode* root, vector<int>& traj) {
        if (nullptr == root) {
            return;
        } else {
            helper(root->left, traj);
            helper(root->right, traj);
            traj.push_back(root->val);
        }
    }
};
