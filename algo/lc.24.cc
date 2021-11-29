/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode* swapPairs(ListNode* head) {
        if (nullptr == head) return head;
        
        ListNode* dummy = new ListNode(-1);
        ListNode* pp = dummy;
        pp->next = head;
        ListNode* p1 = head;
        ListNode* p2 = head->next;
        while(nullptr != p1 && nullptr != p2) {
            ListNode* n = p2->next;
            pp->next = p2;
            p1->next = n;
            p2->next = p1;
            
            pp = p1;
            p1 = pp->next;
            p2 = (nullptr == p1) ? nullptr : p1->next;
        }
        return dummy->next;
    }
};
