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
    vector<int> inorderTraversal(TreeNode* root) {
        /*
        vector<int> traj;
        helper(root, traj);
        return traj;
        */
        vector<int> traj;
        stack<TreeNode*> st;
        
        TreeNode* cur = root;
        while (!st.empty() || cur != nullptr) {
            if (cur != nullptr) {
                st.push(cur);
                cur = cur->left;
            } else { // cur is nullptr
                cur = st.top(); st.pop();
                traj.push_back(cur->val);
                cur = cur->right;
            }
        }
        return traj;
    }
    void helper(TreeNode* root, vector<int>& traj) {
        if (nullptr == root) {
            return;
        } else {
            helper(root->left, traj);
            traj.push_back(root->val);
            helper(root->right, traj);
        }
    }
};

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
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> traj;
        helper(root, traj);
        return traj;
    }
    void helper(TreeNode* root, vector<int>& traj) {
        if (nullptr == root) {
            return;
        } else {
            helper(root->left, traj);
            traj.push_back(root->val);
            helper(root->right, traj);
        }
    }
};
