# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        def get_all_vals(node: Optional[TreeNode]):
            if node is None:
                return []
            elif node.left is None and node.right is None:
                return [node.val]
            else:
                left = get_all_vals(node.left)
                right = get_all_vals(node.right)
                return left + [node.val] + right
        # k-th value (1-indexed)
        return list(sorted(get_all_vals(root)))[k-1]
