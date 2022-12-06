# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if list1 is None and list2 is None:
            return None
        elif list1 is None and list2 is not None:
            return list2
        elif list1 is not None and list2 is None:
            return list1
        # else
        cur1 = list1
        cur2 = list2
        if cur1.val > cur2.val:
            head = ListNode(cur2.val)
            cur2 = cur2.next
        else:
            head = ListNode(cur1.val)
            cur1 = cur1.next
        cursor = head
        while cur1 is not None or cur2 is not None:
            if cur1 is not None and cur2 is not None:
                if cur1.val < cur2.val:
                    cursor.next = ListNode(cur1.val)
                    cur1 = cur1.next
                    cursor = cursor.next
                else:
                    cursor.next = ListNode(cur2.val)
                    cur2 = cur2.next
                    cursor = cursor.next
            elif cur1 is not None:
                cursor.next = ListNode(cur1.val)
                cur1 = cur1.next
                cursor = cursor.next
            else: # cur2 is not None
                cursor.next = ListNode(cur2.val)
                cur2 = cur2.next
                cursor = cursor.next
        return head
