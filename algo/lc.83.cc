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
        // list size >= 2
        if (nullptr == head || nullptr == head->next)
            return head;
        
        ListNode* cur = head->next;
        ListNode* prev = head;
        while(nullptr != cur) {
            if (cur->val == prev->val) {
                // delete the current node
                ListNode* tbr = cur;
                prev->next = cur->next;
                cur = cur->next;
                delete tbr;
            } else {
                // move next
                cur = cur->next;
                prev = prev->next;
            }
        }
        
        return head;
    }
};
