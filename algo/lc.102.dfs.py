# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
import collections
class Solution:
    def dfs(self, node, depth, state):
        if node is None:
            return
        else:
            state[depth].append(node.val)
            self.dfs(node.left, depth+1, state)
            self.dfs(node.right, depth+1, state)
            return

    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        state = collections.defaultdict(list)
        self.dfs(root, 0, state)
        results = []
        for i in range(len(state)):
            results.append(state[i])
        return results
        
