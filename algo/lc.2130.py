# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:

    def getLength(self, node: Optional[ListNode]) -> int:
        if node is None:
            return 0
        else:
            return 1 + self.getLength(node.next)

    def pairSum(self, head: Optional[ListNode]) -> int:
        stack = []
        length = self.getLength(head)
        maxtwin = 0
        cursor = head
        tally = 0
        while cursor is not None:
            if tally < length // 2:
                stack.append(cursor.val)
                tally += 1
            else:
                twinsum = stack.pop(-1) + cursor.val
                maxtwin = max(maxtwin, twinsum)
            cursor = cursor.next
        return maxtwin
