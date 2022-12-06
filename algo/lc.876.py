# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        depth = 1
        cursor = head
        while cursor.next is not None:
            cursor = cursor.next
            depth = depth + 1
        which = depth // 2
        cursor = head
        for _ in range(which):
            cursor = cursor.next
        return cursor
