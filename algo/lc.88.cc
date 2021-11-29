class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        int cur1 = m-1, cur2 = n-1, curh = m+n-1;
        while (cur1 >= 0 && cur2 >= 0) {
            if (nums1[cur1] > nums2[cur2]) {
                nums1[curh] = nums1[cur1];
                curh--;
                cur1--;
            } else { // <=
                nums1[curh] = nums2[cur2];
                curh--;
                cur2--;
            }
        }
        while (cur2 >= 0) {
            nums1[curh] = nums2[cur2];
            curh--;
            cur2--;
        }
    }
};
