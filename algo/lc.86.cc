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
    ListNode* partition(ListNode* head, int x) {
        ListNode ldummy (-1);
        ListNode rdummy (-1);
        ListNode* curl = &ldummy;
        ListNode* curr = &rdummy;
        ListNode* cur  = head;
        
        while (cur != nullptr) {
            if (cur->val < x) {
                ListNode* next = cur->next;
                cur->next = nullptr;
                curl->next = cur;
                curl = curl->next;
                cur = next;
            } else {
                ListNode* next = cur->next;
                cur->next = nullptr;
                curr->next = cur;
                curr = curr->next;
                cur = next;
            }
        }
        curl->next = rdummy.next;
        return ldummy.next;
    }
};
