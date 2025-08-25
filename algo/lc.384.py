class Solution:

    def __init__(self, nums: List[int]):
        self.original = list(nums) # copy

    def reset(self) -> List[int]:
        return self.original

    def shuffle(self) -> List[int]:
        shuffled = list(self.original) # copy
        for i in range(len(shuffled)):
            j = random.randint(0, i)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        return shuffled

# Your Solution object will be instantiated and called as such:
# obj = Solution(nums)
# param_1 = obj.reset()
# param_2 = obj.shuffle()

import random
class Solution:

    def __init__(self, nums: List[int]):
        self.original = list(nums)
        self.length = len(nums)
        
    def reset(self) -> List[int]:
        return self.original
        
    def shuffle(self) -> List[int]:
        rd = [random.random() for _ in range(self.length)]
        argsort = lambda seq: sorted(range(len(seq)), key=seq.__getitem__)
        randidxs = argsort(rd)
        shuffled = [self.original[i] for i in randidxs]
        return shuffled

# Your Solution object will be instantiated and called as such:
# obj = Solution(nums)
# param_1 = obj.reset()
# param_2 = obj.shuffle()
