# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        # flatten list A
        flatA = []
        cur = headA
        while cur is not None:
            flatA.append(cur)
            cur = cur.next
        # flatten list B
        flatB = []
        cur = headB
        while cur is not None:
            flatB.append(cur)
            cur = cur.next
        # reverse
        flatA = flatA[::-1]
        flatB = flatB[::-1]
        # compare
        intersect = None
        if flatA[0] != flatB[0]:
            return None
        cursor = 0
        while flatA[cursor] == flatB[cursor]:
            intersect = flatA[cursor]
            cursor = cursor + 1
            if cursor >= min(len(flatA), len(flatB)):
                break
        return intersect
        
