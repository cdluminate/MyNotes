# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:

    def getLeaves(self, root: Optional[TreeNode]) -> List[TreeNode]:
        if root is None:
            return []
        elif root.left is None and root.right is None:
            return [root]
        else:
            leftleaves = self.getLeaves(root.left)
            rightleaves = self.getLeaves(root.right)
            leaves = leftleaves + rightleaves
            return leaves

    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        leaves1 = self.getLeaves(root1)
        leaves2 = self.getLeaves(root2)
        vals1 = [x.val for x in leaves1]
        vals2 = [x.val for x in leaves2]
        #print(leaves2)
        return vals1 == vals2
