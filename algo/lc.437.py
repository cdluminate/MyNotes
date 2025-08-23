# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        if root is None:
            return 0
        # case 1: count current node
        current = self.dfs(root, targetSum)
        # case 2: do not count current node
        left = self.pathSum(root.left, targetSum)
        right = self.pathSum(root.right, targetSum)
        return current + left + right
    def dfs(self, root: Optional[TreeNode], targetSum: int) -> int:
        if root is None:
            return 0
        result = 1 if root.val == targetSum else 0
        result += self.dfs(root.left, targetSum - root.val)
        result += self.dfs(root.right, targetSum - root.val)
        return result
            

