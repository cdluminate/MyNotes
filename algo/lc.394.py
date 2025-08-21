class Solution:
    def seekSqr(self, string: str):
        state = 0 # depth
        for i, char in enumerate(string):
            if char == '[':
                state += 1
            elif char == ']':
                state -= 1
                if state == 0:
                    return i
            else:
                pass
        return len(string) - 1

    def seekK(self, string: str, probe: int):
        while string[probe] in '0123456789':
            if probe == 0:
                return probe
            elif string[probe-1] not in '0123456789':
                return probe
            else:
                probe -= 1
    
    def decodeOne(self, string: str) -> str:
        # parse: left, k, [, substr, ], right
        #print('>', string)
        idx_sql = string.index('[')
        idx_sqr = self.seekSqr(string)
        right = string[idx_sqr+1:]
        substr = string[idx_sql+1:idx_sqr]
        idx_k = self.seekK(string, idx_sql-1)
        k = int(string[idx_k:idx_sql])
        left = string[:idx_k]
        if '[' not in substr:
            middle = substr * k
        else:
            middle = self.decodeOne(substr) * k
        #print('<', k, middle)
        return left + middle + right

    def decodeString(self, s: str) -> str:
        tmp = s
        while '[' in tmp:
            tmp = self.decodeOne(tmp)
        return tmp
