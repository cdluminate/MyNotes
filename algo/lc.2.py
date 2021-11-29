# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        # we assume the input list length > 0
        # we find that the length of the two input number may differ
        carry = 0
        head = ListNode( (l1.val+l2.val+carry)%10 )
        cursor = head
        carry = (l1.val+l2.val+carry)//10
        l1 = l1.next
        l2 = l2.next
        while (l1 != None or l2 != None):
            if l1 == None:
                tmp = l2.val + carry
            elif l2 == None:
                tmp = l1.val + carry
            else:
                tmp = l1.val + l2.val + carry
            newnode = ListNode( tmp%10 )
            carry = tmp//10
            cursor.next = newnode
            cursor = newnode
            if l1 != None: l1 = l1.next
            if l2 != None: l2 = l2.next
        # clear the carry bit
        if carry != 0:
            newnode = ListNode( carry )
            cursor.next = newnode
            cursor = newnode
        return head
