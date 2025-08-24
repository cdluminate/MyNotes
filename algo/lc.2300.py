class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        n = len(spells)
        m = len(potions)
        potions.sort()
        pairs = [None for _ in range(n)]
        for i in range(n):
            bound = [0, len(potions) - 1]
            first_valid_idx = len(potions)
            while bound[0] <= bound[1]:
                mid = bound[0] + (bound[1] - bound[0]) // 2
                if potions[mid] * spells[i] >= success:
                    first_valid_idx = mid
                    bound = [bound[0], mid - 1]
                else: # < success
                    bound = [mid + 1, bound[1]]
            #print(spells[i], first_valid_idx)
            pairs[i] = len(potions) - first_valid_idx
        return pairs

class Solution:
    def locate(self, arr: List[int], thresh: int) -> int:
        # the index of the last item in arr that is < thresh
        # note, the arr is a sorted array, ascending.
        bound = [0, len(arr) - 1]
        attempt = sum(bound) // 2
        while True:
            if arr[attempt] >= thresh:
                # move left, [keep, attempt)
                bound = [bound[0], attempt]
                attempt = sum(bound) // 2
            elif arr[attempt] < thresh:
                # end criterion: we found the index
                if attempt >= len(arr) - 1 or arr[attempt+1] >= thresh:
                    return attempt
                # move right, (attempt, keep]
                else:
                    bound = [attempt, bound[1]]
                    attempt = 1 + sum(bound) // 2

    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        n = len(spells)
        m = len(potions)
        potions.sort()
        pairs = [None for _ in range(n)]
        for i in range(n):
            threshold = success / spells[i]
            midpotion = self.locate(potions, threshold)
            pairs[i] = len(potions) - midpotion -1
        return pairs

# XXX: time out
class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        n = len(spells)
        m = len(potions)
        pairs = [None for _ in range(n)]
        for i in range(n):
            threshold = success / spells[i]
            pairs[i] = sum([1 for x in potions if x >= threshold])
        return pairs
