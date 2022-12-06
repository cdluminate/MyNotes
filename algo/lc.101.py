# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def compare(self, left: Optional[TreeNode], right: Optional[TreeNode]) -> bool:
        if left is None and right is None:
            return True
        elif left is None or right is None:
            return False
        else: # left is not None and right is not None:
            if left.val != right.val:
                return False
            return self.compare(left.left, right.right) \
                    and self.compare(left.right, right.left)
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        return self.compare(root.left, root.right)
