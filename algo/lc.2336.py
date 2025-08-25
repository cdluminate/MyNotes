class SmallestInfiniteSet:

    def __init__(self):
        self.used = dict()

    def popSmallest(self) -> int:
        cursor = 1
        while cursor in self.used:
            cursor += 1
        self.used[cursor] = True
        return cursor

    def addBack(self, num: int) -> None:
        if num in self.used:
            self.used.pop(num)
        


# Your SmallestInfiniteSet object will be instantiated and called as such:
# obj = SmallestInfiniteSet()
# param_1 = obj.popSmallest()
# obj.addBack(num)
