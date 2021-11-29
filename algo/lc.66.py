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
