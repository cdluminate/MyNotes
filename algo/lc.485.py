# array

a = [1,1,0,1,1,1]
b = ''.join(map(str, a))
c = b.split('0')
d = [len(x) for x in c]
print(max(d))

class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        s = ''.join(map(str, nums)).split('0')
        return max([len(x) for x in s])
