# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        self.result = None
        self.found = False
        def dfs(node, state: List[int]) -> List[int]:
            if node is None or self.found:
                return state
            elif node.left is None and node.right is None:
                return state + [node.val]
            else:
                lstate = dfs(node.left, [])
                rstate = dfs(node.right, [])
                state = lstate + rstate + [node.val]
                #print('>', state)
                if p.val in state and q.val in state:
                    #print('it is', node.val)
                    if self.result is None:
                        self.result = node
                        self.found = True
                return state
        dfs(root, [])
        return self.result
            
