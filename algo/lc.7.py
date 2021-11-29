class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        tmp = abs(x)
        sign = (x>0) and 1 or -1
        places = []
        # parse the integer
        while tmp > 0:
          places.append(tmp%10)
          tmp = int(tmp/10)
        # generate new integer
        for i in places:
          tmp = tmp*10 + i
        if tmp>2**31-1: return 0 # 32-bit *signed* int may overflow
        return tmp*sign

solution = Solution()
print(solution.reverse(123))
print(solution.reverse(-123))
print(solution.reverse(1534236469))

# accepted
