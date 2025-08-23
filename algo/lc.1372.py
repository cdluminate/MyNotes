# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        self.result = 0
        def dfs(node, state, depth):
            if node is None:
                return
            # update max
            self.result = max(self.result, depth + 1)
            # case 1: go left
            if state == 0:
                # case 1.1 continue
                dfs(node.left, 1, depth+1)
                # case 1.2 start over
                dfs(node.right, 0, 1)
            # case 2: go right
            else:
                # case 2.1 continue
                dfs(node.right, 0, depth+1)
                # case 2.2 start over
                dfs(node.left, 1, 1)
        dfs(root.left, 1, 1)
        dfs(root.right, 0, 1)
        return max(0, self.result - 1)


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def dfs(self, node: Optional[TreeNode], state: int) -> int:
        # zig zag tree depth
        if node is None:
            return 0
        elif state == 0:
            # go left for the current step
            return 1 + self.dfs(node.left, 1)
        else:
            # go right for the current step
            return 1 + self.dfs(node.right, 0)
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        # case 1: include the current node
        left_incl = self.dfs(root, 0)
        right_incl = self.dfs(root, 1)
        max_incl = max(left_incl, right_incl) - 1
        # case 2: exclude the current node
        left_excl = self.longestZigZag(root.left)
        right_excl = self.longestZigZag(root.right)
        max_excl = max(left_excl, right_excl)
        return max(max_incl, max_excl)
