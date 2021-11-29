class Solution {
public:
    int strStr(string haystack, string needle) {
        if (0==needle.size() && 0==haystack.size()) return 0;
        if (0==needle.size()) return 0;
        if (0==haystack.size()) return -1;
        if (needle.size() > haystack.size()) return -1;
        
        for (int i = 0; i < haystack.size()-needle.size()+1; i++) {
            int j = 0;
            while (j < needle.size() && haystack[i+j]==needle[j]) {
                j++;
            }
            if (needle.size() == j)
                return i;
        }
        return -1;
    }
};

class Solution {
public:
    int strStr(string haystack, string needle) {
        if (0==needle.size() && 0==haystack.size()) return 0;
        if (0==needle.size()) return 0;
        if (0==haystack.size()) return -1;
        if (needle.size() > haystack.size()) return -1;

        for (int i = 0; i < haystack.size()-needle.size()+1; i++) {
            for (int j = 0; j < needle.size(); j++) {
                if (haystack[i+j] != needle[j]) break;
                if (j == needle.size() - 1) return i;
            }
        }
        return -1;
    }
};
