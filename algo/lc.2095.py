# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:

    def getDepth(self, head: ListNode) -> int:
        if head.next is None:
            return 0
        else:
            return 1 + self.getDepth(head.next)

    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        depth = self.getDepth(head)
        if depth == 0:
            return None
        # seek the middle one
        cur, nex = head, head.next
        steps = (depth // 2) if depth%2==1 else depth//2-1
        for i in range(steps):
            cur, nex = nex, nex.next
            print(i, cur.val, nex.val)
        # perform surgery
        cur.next = nex.next
        return head

        
