class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        if n == 0:
            return ['']
        elif n == 1:
            return ['()']
        else:
            ret = []
            for c in range(n):
                for left in self.generateParenthesis(c):
                    for right in self.generateParenthesis(n-c-1):
                        ret.append(f'({left}){right}')
            return ret
