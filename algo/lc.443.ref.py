class Solution:
    def compress(self, chars: List[str]) -> int:
        n = len(chars)
        if n <= 1:
            return n
        read_cursor = 0
        write_cursor = 0
        while read_cursor < n:
            # go through segment
            j = read_cursor
            while j < n and chars[read_cursor] == chars[j]:
                j += 1
            count = j - read_cursor
            # write back
            chars[write_cursor] = chars[read_cursor]
            write_cursor += 1
            if count > 1:
                for digit in str(count):
                    chars[write_cursor] = digit
                    write_cursor += 1
            read_cursor = j
        return write_cursor

