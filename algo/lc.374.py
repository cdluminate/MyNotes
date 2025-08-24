# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num: int) -> int:

class Solution:
    def guessNumber(self, n: int) -> int:
        # answer is in [1, n]
        bound = [1, n]
        attempt = sum(bound) // 2
        while (response := guess(attempt)) != 0:
            #print(bound, attempt, response)
            if response == -1:
                # answer is in [keep, attempt)
                bound = [bound[0], attempt]
                attempt = sum(bound) // 2
            elif response == 1:
                # attempt is in (attempt, keep]
                bound = [attempt, bound[1]]
                attempt = (1 + sum(bound)) // 2
            else:
                raise Exception('should not happen')
        return attempt
