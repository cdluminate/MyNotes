# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:

    def keyInTree(self, root, key):
        if root is None:
            return False
        elif root.val == key:
            return True
        elif root.val < key:
            return self.keyInTree(root.right, key)
        else:
            return self.keyInTree(root.left, key)

    def locateNode(self, root: Optional[TreeNode], key: int, parent = None):
        # return (node, parent)
        if root is None:
            return [None, None]
        elif root.val == key:
            return [root, parent]
        elif root.val < key:
            # go right
            return self.locateNode(root.right, key, root)
        elif root.val > key:
            # go left
            return self.locateNode(root.left, key, root)
        else:
            raise Exception("should not happen")

    def rebuild(self, root: Optional[TreeNode]):
        if root is None:
            return None
        # collect numbers excluding root
        numbers = []
        def dfs(node) -> None:
            if node is None:
                return
            else:
                dfs(node.left)
                numbers.append(node.val)
                dfs(node.right)
        dfs(root)
        numbers.pop(numbers.index(root.val))
        # rebuild the tree by exluding the root
        def tree(numbers) -> TreeNode:
            if not numbers:
                return None
            elif len(numbers) == 1:
                return TreeNode(numbers[0], None, None)
            else:
                idx = len(numbers) // 2
                left = tree(numbers[:idx])
                right = tree(numbers[idx+1:])
                return TreeNode(numbers[idx], left, right)
        return tree(numbers)

    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if root is None:
            return None
        if not self.keyInTree(root, key):
            return root
        node, parent = self.locateNode(root, key)
        # case 1: it is root
        if parent is None:
            return self.rebuild(node)
        # case 2: it is left of parent
        elif parent.left and parent.left.val == key:
            parent.left = self.rebuild(node)
            return root
        # case 3: it is right of parent
        elif parent.right and parent.right.val == key:
            parent.right = self.rebuild(node)
            return root
        else:
            raise Exception("should not happen")

