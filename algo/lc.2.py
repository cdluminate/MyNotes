# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        cur1, cur2 = l1, l2
        head = ListNode()
        res = head
        carry = 0
        while (cur1 is not None) or (cur2 is not None):
            cur1_val = cur1.val if cur1 is not None else 0
            cur2_val = cur2.val if cur2 is not None else 0
            res.val = (cur1_val + cur2_val + carry) % 10
            carry = (cur1_val + cur2_val + carry) // 10
            cur1 = cur1.next if cur1 is not None else None
            cur2 = cur2.next if cur2 is not None else None
            if (cur1 is not None) or (cur2 is not None):
                res.next = ListNode()
                res = res.next
            elif (cur1 is None) and (cur2 is None) and (carry != 0):
                res.next = ListNode(carry)
        return head
