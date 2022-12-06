class Solution(object):
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        carry = 0
        for i in reversed(range(len(digits))):
            if i == len(digits)-1:
                digits[i] += 1
            else:
                digits[i] += carry
            carry = int(digits[i] / 10)
            digits[i] %= 10
        if carry>0:
            digits.insert(0, carry)
        return digits

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        ret = digits[::-1]
        ret[0] = ret[0] + 1
        for i in range(1,len(digits)):
            if ret[i-1] > 9:
                tmp = ret[i-1]
                ret[i-1] = tmp % 10
                ret[i] = ret[i] + (tmp // 10)
        if ret[-1] > 9:
            tmp = ret[-1]
            ret[-1] = tmp % 10
            ret.append(tmp // 10)
        return ret[::-1]
