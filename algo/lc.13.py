class Solution:
    def romanToInt(self, s: str) -> int:
        sv = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        lex = []
        while len(s) > 0:
            if len(s) > 1 and sv[s[0]] < sv[s[1]]:
                # special combination
                lex.append(s[:2])
                s = s[2:]
            else:
                # normal case
                lex.append(s[0])
                s = s[1:]
        res = 0
        for token in lex:
            if len(token) == 1:
                # normal case
                res = res + sv[token]
            else:
                # special case (2 char)
                val = sv[token[1]] - sv[token[0]]
                res = res + val
        return res
        
