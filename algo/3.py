class Solution(object):
  def lengthOfLongestSubstring(self, s):
    """
    :type s: str
    :rtype: int
    """
    ans = ''
    # left cursor
    for cursorl in range(len(s)):
      # right cursor
      for cursorr in range(cursorl, len(s)):
        candidate = s[cursorl:cursorr+1]
        if len(candidate)<=len(ans): continue
        if len(list(set(candidate))) == len(list(candidate)) and len(candidate)>len(ans):
          print('{} {}'.format(cursorl, cursorr))
          print('candidate {} longer'.format(candidate))
          ans = candidate
    return len(ans)
          
solution = Solution()
print(solution.lengthOfLongestSubstring("abcabcbb"))
print(solution.lengthOfLongestSubstring("bbbbb"))
print(solution.lengthOfLongestSubstring("pwwkew"))
print(solution.lengthOfLongestSubstring("c"))
print(solution.lengthOfLongestSubstring("au"))

# time out
