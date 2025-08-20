class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        highest = 0
        current = 0
        for x in gain:
            current += x
            highest = max(current, highest)
        return highest
