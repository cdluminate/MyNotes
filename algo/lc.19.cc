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
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        if (nullptr == head) return head;
        
        ListNode* dummy = new ListNode(-1);
        dummy->next = head;
        ListNode* prev = dummy;
        ListNode* cur  = head;
        ListNode* det  = head;
        
        for (int i = 0; i < n; i++)
            det = det->next;
        while(nullptr != det) {
            det = det->next;
            prev = prev->next;
            cur = cur->next;
        }
        // cur: tbr
        
        prev-> next = cur->next;
        delete cur;
        return dummy->next;
    }
};
