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
    ListNode* deleteDuplicates(ListNode* head) {
        if (nullptr == head) return head;
        
        ListNode* dummy = new ListNode(-1);
        dummy->next = head;
        ListNode* cur = head;
        ListNode* prev = dummy;
        ListNode* tail = cur;
        
        while (nullptr != cur) {
            // is the current node duplicated?
            tail = cur;
            if (nullptr != cur->next && cur->val == cur->next->val) {
                while (nullptr != tail && tail->val == cur->val)
                    tail = tail->next;
                // TODO: free the deleted nodes
                prev->next = tail;
                cur = tail;
            } else {
                prev = prev->next;
                cur = cur->next;
            }
        }
        
        return dummy->next;
    }
};
