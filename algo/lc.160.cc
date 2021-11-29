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
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        /*
        if (nullptr == headA || nullptr == headB) return nullptr;
        
        // traverse list A, and memorize the nodes
        map<ListNode*, bool> mA;
        ListNode* cur = headA;
        while (cur != nullptr) {
            mA[cur] = true;
        }
        // traverse list B, see if there is any node appeard in list A
        cur = headB;
        map<ListNode*, bool>::iterator mApos;
        while (cur != nullptr) {
            if ((mApos = mA.find(cur)) != mA.end()) {
                return cur;
            }
            cur = cur->next;
        }
        // no intersection at all
        return nullptr; // timeout
        */
        
        if (nullptr == headA || nullptr == headB) return nullptr;
        
        // get len(A) and len(B)
        int lenA = 0, lenB = 0;
        ListNode* curA = headA, * curB = headB;
        while (curA != nullptr) {
            curA = curA -> next;
            lenA++;
        }
        while (curB != nullptr) {
            curB = curB -> next;
            lenB++;
        }
        // the cursor of the longest list go first by (m-n) steps
        curA = headA;
        curB = headB;
        if (lenA != lenB) {
            int s = max(lenA, lenB) - min(lenA, lenB);
            if (lenA > lenB) {
                for (int i = 0; i < s; i++) curA = curA->next;
            } else { // lenA < lenB
                for (int i = 0; i < s; i++) curB = curB->next;
            }
        }
        // move A and B together and see wether they meet
        while (curA != nullptr && curB != nullptr) {
            if (curA == curB) {
                return curA;
            } else {
                curA = curA -> next;
                curB = curB -> next;
            }
        }
        // they didn't meet each other
        return nullptr;
    }
};
