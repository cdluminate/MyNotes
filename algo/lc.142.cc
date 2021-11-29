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
    ListNode *detectCycle(ListNode *head) {
        /*
        if (nullptr == head) return head;
        
        ListNode* cur = head;
        map<ListNode*, bool> m;
        map<ListNode*, bool>::iterator pos;
        
        while (cur != nullptr) {
            if ((pos = m.find(cur)) != m.end()) {
                return cur;
            }
            m[cur] = true;
        }
        return nullptr; // trouble
        */
		/* i: iter, x: head to cycle entrance
		 * a: entrance to meet, r: cycle len
		 *
		 * 2i = x + a + nr
		 *  i = x + a
		 * => x = nr - a
		 */
        ListNode* cur = head, *fast = head;
        while (fast && fast->next) {
            cur = cur->next;
            fast = fast->next->next;
            
            if (cur == fast) {
                ListNode* p = head;
                while (p != cur) {
                    p = p->next;
                    cur = cur->next;
                }
                return p;
            }
        }
        return nullptr;
    }
};
