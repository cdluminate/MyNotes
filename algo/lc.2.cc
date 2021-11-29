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
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* p1 = l1;
        ListNode* p2 = l2;
        
        ListNode* head = new ListNode(-1); // dummy
        ListNode* cur = head;
        
        int carry = 0;
        while(p1 != nullptr || p2 != nullptr) {
            int v = carry;
            v += (nullptr == p1) ? 0 : p1-> val;
            v += (nullptr == p2) ? 0 : p2-> val;
            carry = v / 10;
            cur-> next = new ListNode(v % 10);
            cur = cur->next;
            
            p1 = (nullptr == p1) ? p1 : p1->next;
            p2 = (nullptr == p2) ? p2 : p2->next;
        }
        if (carry > 0) {
            cur->next = new ListNode(carry);
        }
        return head->next;
    }
};
