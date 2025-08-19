class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        maxarea = 0
        while left < right:
            # process the current area
            w = right - left
            h = min(height[left], height[right])
            area = w * h
            maxarea = area if area > maxarea else maxarea
            # move the short bar
            if height[left] <= height[right]:
                left += 1
            else: # height[left] > height[right]:
                right -= 1
        return maxarea

class Solution:
    def maxArea(self, height: List[int]) -> int:
        maxarea = 0
        for i in range(len(height)):
            for j in range(i, len(height)):
                width = j - i
                h = min(height[i], height[j])
                area = width * h
                maxarea = area if area > maxarea else maxarea
        return maxarea
