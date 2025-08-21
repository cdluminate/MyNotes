# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def countgood(node: Optional[TreeNode], sofarmax: int) -> int:
            if node is None:
                return 0
            elif node.left is None and node.right is None:
                return 1 if node.val >= sofarmax else 0
            else:
                selfcount = 1 if node.val >= sofarmax else 0
                sofarmax = max(sofarmax, node.val)
                leftcount = countgood(node.left, sofarmax)
                rightcount = countgood(node.right, sofarmax)
                return selfcount + leftcount + rightcount
        return countgood(root, root.val)

