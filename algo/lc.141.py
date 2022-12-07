# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        fast = head
        slow = head
        while True:
            fast = fast.next if fast is not None else None
            if fast is None or slow is None:
                return False
            elif fast == slow:
                return True
            else:
                fast = fast.next
                slow = slow.next
