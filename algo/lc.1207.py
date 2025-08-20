from collections import Counter
class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        count = Counter(arr)
        values = list(count.values())
        return len(set(values)) == len(values)
