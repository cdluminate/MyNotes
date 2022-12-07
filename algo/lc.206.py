# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return None
        elif head.next is None:
            return head
        else:
            left = head
            right = self.reverseList(head.next)
            cur = right
            while cur.next is not None:
                cur = cur.next
            cur.next = left
            left.next = None
            return right
