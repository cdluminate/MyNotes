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
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> traj;
        preordertraversal(root, traj);
        return traj;
    }
    void preordertraversal(TreeNode* root, vector<int>& traj) {
        if (nullptr == root) {
            return;
        } else {
            traj.push_back(root->val);
            preordertraversal(root->left, traj);
            preordertraversal(root->right, traj);
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
    vector<int> preorderTraversal(TreeNode* root) {
        /*
        vector<int> traj;
        preordertraversal(root, traj);
        return traj;
        */
        vector<int> traj;
        stack<TreeNode*> st;
        
        if (root != nullptr) st.push(root);
        while (!st.empty()) {
            TreeNode* cur = st.top(); st.pop();
            traj.push_back(cur->val);
            
            if (nullptr != cur->right) st.push(cur->right);
            if (nullptr != cur->left)  st.push(cur->left);
        }
        return traj;
    }
    void preordertraversal(TreeNode* root, vector<int>& traj) {
        if (nullptr == root) {
            return;
        } else {
            traj.push_back(root->val);
            preordertraversal(root->left, traj);
            preordertraversal(root->right, traj);
        }
    }
};
