class Solution:

    def plantOne(self, flowerbed: List[int]) -> bool:
        # go thorugh every slot
        for i in range(len(flowerbed)):
            if flowerbed[i] == 1:
                # check the next spot if empty
                continue
            else:
                # if empty, check the surroundings
                left_ok = flowerbed[i-1] == 0 if i-1>=0 else True
                right_ok = flowerbed[i+1] == 0 if i+1<len(flowerbed) else True
                if left_ok and right_ok:
                    # valid position. plant it
                    flowerbed[i] = 1
                    return True
                else:
                    # invalid position. skip
                    continue
        # gone through all spots without planting
        return False

    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        tmp = list(flowerbed)
        # case: clearly invalid overlength
        if n > 1 + len(tmp) // 2:
            return False
        # case: clearly invalid no so many slots
        if n > sum([1 for x in tmp if x == 0]):
            return False
        # plant the n flowers one by one
        for _ in range(n):
            if not self.plantOne(tmp):
                return False
        # all planted
        return True
