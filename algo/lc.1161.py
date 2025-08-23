# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        levelsums = []
        # find all level sums
        queue = [root]
        while queue:
            # get the current level
            to_traverse = [queue.pop(0) for _ in range(len(queue))]
            # find the sum of the current level
            cur_sum = sum([x.val for x in to_traverse])
            levelsums.append(cur_sum)
            # prepare the next level
            for node in to_traverse:
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        # match the first max level sum
        maxsum = max(levelsums)
        return levelsums.index(maxsum) + 1
