class Solution {
public:
    bool isValid(string s) {
        string left="([{";
        string right=")]}";
        stack<char> st;
        
        for (auto c : s) {
            if (left.find(c) != string::npos) { // left parenthis
                st.push(c);
            } else { // right parenthis
                if (st.empty())
                    return false;
                else if (st.top() != left[right.find(c)])
                    return false;
                else
                    st.pop();
            }
        }
        return st.empty();
    }
};
