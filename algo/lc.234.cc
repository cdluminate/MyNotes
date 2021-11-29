#include <iostream>
#include <vector>
#include <stack>
using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
	ListNode(int x, ListNode* y) : val(x), next(y) {}
};

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
    bool isPalindrome(ListNode* head) {
        if (nullptr == head) return true;
        
        stack<int> st;
        int len = 0;
        ListNode* cur = head;
        
        // get length
        while (cur != nullptr) {
            cur = cur->next;
            len++;
        }
		//cout << "list length " << len << endl;
        // push half of the list to stack
        cur = head;
        for (int i = 0; i < len/2; i++) {
            st.push(cur->val);
			//cout << "pushed " << cur->val << endl;
			cur = cur->next; // XXX: this line matters!
        }
        // skip the middle node if len is odd
        if (len%2 == 1) cur = cur -> next;
        // go on and check with stack
        while (cur != nullptr) {
            if (cur->val != st.top()) {
                return false;
            } else {
                cur = cur->next;
                st.pop();
            }
        }
        // valid
        return true; // O(n) S(n)
    }
};

// O(n) S(1) : reverse the second half of the list, then compare

int
main(void)
{
	auto s = Solution();

	auto a1 = ListNode(1);
	auto a2 = ListNode(2, &a1);
	auto a3 = ListNode(3, &a2);
	auto a4 = ListNode(2, &a3);
	auto a5 = ListNode(1, &a4);

	auto b1 = ListNode(1);

	auto c1 = ListNode(1);
	auto c2 = ListNode(2, &c1);
	
	cout << "=> " << s.isPalindrome(&a5) << endl;
	cout << "=> " << s.isPalindrome(&b1) << endl;
	cout << "=> " << s.isPalindrome(&c2) << endl;

	return 0;
}
