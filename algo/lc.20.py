class Solution:
    def isValid(self, s: str) -> bool:
        special = '(){}[]'
        stack = []
        for char in s:
            if char in special:
                if char in '([{':
                    # begin
                    stack.append(char)
                else:
                    # end
                    if not stack:
                        return False
                    if char == ')' and stack[-1] == '(':
                        stack.pop(-1)
                    elif char == ']' and stack[-1] == '[':
                        stack.pop(-1)
                    elif char == '}' and stack[-1] == '{':
                        stack.pop(-1)
                    else:
                        return False
        return not stack
