class Solution {
public:
    int lengthOfLastWord(string s) {
        if (s.empty()) return 0;
        bool hasalpha = false;
        for (int i = 0; i < s.size(); i++) {
            if (isalpha(s[i])) hasalpha = true;
        }
        if (!hasalpha)
            return 0;
        
        int lastr = s.size()-1;
        while (lastr >= 0 && !isalpha(s[lastr]))
            lastr--;
        int lastl = lastr;
        while (lastl >= 0 && isalpha(s[lastl]))
            lastl--;
        
        return lastr - lastl;
    }
};
