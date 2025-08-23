# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        view = []
        queue = [root]
        while queue:
            to_traverse = [queue.pop(0) for _ in range(len(queue))]
            # find the rightmost view
            view.append(to_traverse[-1].val)
            # go to next layer
            for n in to_traverse:
                if n.left is not None:
                    queue.append(n.left)
                if n.right is not None:
                    queue.append(n.right)
        return view
            
