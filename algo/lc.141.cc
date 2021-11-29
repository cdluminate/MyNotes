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
    bool hasCycle(ListNode *head) {
        if (nullptr == head) return head;
        
        ListNode* fast = head;
        ListNode* slow = head;
        while(fast != nullptr && slow != nullptr) {
            slow = slow->next;
            fast = (fast==nullptr) ? nullptr : fast->next;
            fast = (fast==nullptr) ? nullptr : fast->next;
            if (fast != nullptr && fast == slow) {
                return true;
            }
        }
        return false;
    }
};
