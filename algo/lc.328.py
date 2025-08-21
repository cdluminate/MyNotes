# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return head
        leftH, left = head, head
        rightH, right = head.next, head.next
        while (right is not None and right.next is not None):
            left.next = right.next
            left = right.next
            right.next = left.next
            right = left.next
        left.next = rightH
        return leftH
