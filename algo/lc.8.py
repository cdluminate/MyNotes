class Solution(object):
    def myAtoi(self, string):
        """
        :type str: str
        :rtype: int
        """
        # round 0: handle special case, preprocess
        if len(string)==0: return 0
        string = string.strip()
        # round 1: filtering
        res = []
        for (k,token) in enumerate(string):
          if k==0 and (token=='+' or token=='-'):
            res.append(token)
            continue
          else:
            if token.isdigit():
              res.append(token)
            else:
              break
        # round 2: assemble, handle special condition and parse
        res = ''.join(res)
        if len(res)==0: return 0
        if res=='+': return 0
        if res=='-': return 0
        if int(res)>2147483647: return 2147483647 # int32 upper bound
        if int(res)<-2147483648: return -2147483648 # int32 lower bound
        return int(res)

solution = Solution()
print(solution.myAtoi('23234'))
print(solution.myAtoi('-23234'))
print(solution.myAtoi('232asdf34'))
print(solution.myAtoi('232-34'))

# Accepted
