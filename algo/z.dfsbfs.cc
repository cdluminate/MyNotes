#include <iostream>
#include <vector>
#include <queue>
using namespace std;

struct TreeNode {
	int val;
	TreeNode* left;
	TreeNode* right;
	TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

// Depth-First-Search
void dfs(TreeNode* root) {
	if (root==nullptr) { // boundary
		return;
	} else {
		cout << root->val << endl;
		dfs(root->left);
		dfs(root->right);
	}
}

// Depth-First-Search, Iterative
void dfs_iter(TreeNode* root) {
	TreeNode* cursor = root;
	vector<TreeNode*> st;
	if (cursor != nullptr) st.push_back(root);
	while (!st.empty()) {
		cursor = st.back(); st.pop_back();
		cout << cursor->val << endl;
		if (cursor->right) st.push_back(cursor->right);
		if (cursor->left) st.push_back(cursor->left);
	}
}

// Breadth-First-Search
void bfs(TreeNode* root) {
	queue<TreeNode*> q;
	TreeNode* cursor = root;
	if (root != nullptr) q.push(cursor);
	while (!q.empty()) {
		cursor = q.front(); q.pop();
		cout << cursor->val << endl;
		if (cursor->left) q.push(cursor->left);
		if (cursor->right) q.push(cursor->right);
	}
}

int
main(void) {
	TreeNode a (0);
	TreeNode b (1);
	TreeNode c (2);
	a.left = &b; a.right = &c;
	TreeNode d (3);
	TreeNode e (4);
	b.left = &d; b.right = &e;
	TreeNode f (5);
	TreeNode g (6);
	c.left = &f; c.right = &g;

	cout << "DFS" << endl;
	dfs(&a); // 0 1 3 4 2 5 6

	cout << "DFS (iter)" << endl;
	dfs_iter(&a); // 0 1 3 4 2 5 6

	cout << "BFS" << endl;
	bfs(&a); // 0 1 2 3 4 5 6

	return 0;
}
