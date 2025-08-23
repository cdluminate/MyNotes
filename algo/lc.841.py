class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        cur_keys = rooms[0]
        cur_rooms = list(range(1, len(rooms)))

        # there are still keys and rooms
        while cur_keys and cur_rooms:
            # open the rooms with all keys we have
            new_keys = []
            for k in cur_keys:
                if k not in cur_rooms:
                    continue
                cur_rooms.pop(cur_rooms.index(k))
                new_keys.extend(rooms[k])
            cur_keys = new_keys

        # we run out of keys. Let's see the remaining rooms
        if cur_rooms:
            return False
        else:
            return True
