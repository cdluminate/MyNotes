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
    ListNode* rotateRight(ListNode* head, int k) {
        if (nullptr == head) return head;
        
        // get list length
        int length = 1;
        ListNode* cur = head;
        while (cur->next != nullptr) {
            length++;
            cur = cur->next;
        }
        k = k % length;
        
        // make a ring
        cur->next = head;
        
        // cut at len-k | len-k+1
        for (int i = 0; i < length-k; i++) {
            cur = cur->next;
        }
        head = cur->next;
        cur->next = nullptr;
        
        return head;
    }
};
