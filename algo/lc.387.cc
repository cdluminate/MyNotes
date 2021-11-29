class Solution {
public:
    int firstUniqChar(string s) {
        map<char, int> counter;
        // create dictionary
        for (auto i : s) {
            auto cursor = counter.find(i);
            if (cursor != counter.end()) {
                cursor->second += 1;
            } else {
                counter.insert(pair<char, int>(i, 1));
            }
        }
        // scan
        for (int i = 0; i < s.size(); i++) {
            auto cursor = counter.find(s[i]);
            if (cursor->second == 1)
                return i;
        }
        return -1;
    }
};
