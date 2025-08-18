from collections import OrderedDict
class LRUCache:

    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key in self.cache:
            value = self.cache[key]
            self.cache.move_to_end(key)
            return value
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        # case: key exists, no length change
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
        # case: key does not exist, cache not full
        elif key not in self.cache and len(self.cache) < self.capacity:
            self.cache[key] = value
            self.cache.move_to_end(key)
        # case: key does not exist, cache full
        else:
            self.cache.popitem(last=False)
            self.cache[key] = value
            self.cache.move_to_end(key)


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
