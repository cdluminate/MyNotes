class LRUCache:

    def __init__(self, capacity: int):
        self.cache = {} # Dict[int,List[int, int]]
        self.capacity = capacity
        self.timestamp = 0

    def get(self, key: int) -> int:
        # case: cache hit
        if key in self.cache:
            self.cache[key][0] = self.timestamp
            self.timestamp += 1
            return self.cache[key][-1]
        # case: not available
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        # case: key does not exist and cache not full
        if key not in self.cache and len(self.cache) < self.capacity:
            self.cache[key] = [self.timestamp, value]
            self.timestamp += 1
        # case: key does not exist and cache full
        elif key not in self.cache and len(self.cache) == self.capacity:
            keyoldest = min(self.cache.keys(), key=lambda x: self.cache[x][0])
            self.cache.pop(keyoldest)
            self.cache[key] = [self.timestamp, value]
        # case: key exists
        elif key in self.cache:
            self.cache[key] = [self.timestamp, value]
        else:
            raise Exception('should not happen')
        self.timestamp += 1

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
