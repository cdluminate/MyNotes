class Solution:
    def compress(self, chars: List[str]) -> int:
        if not chars:
            return 0
        state = (None, 0)  # char, tally
        cursor = 0
        # start state machine
        for c in chars:
            if state[0] is None:
                # initialize state
                state = (c, 1)
            elif state[0] == c:
                # accumulate character tally
                state = (state[0], state[1] + 1)
            else:
                # character changed, write changes
                if state[1] == 1:
                    chars[cursor] = state[0]
                    cursor += 1
                else:
                    chars[cursor] = state[0]
                    nlen = len(str(state[1]))
                    chars[cursor+1:cursor+nlen+1] = str(state[1])
                    cursor += 1 + nlen
                # update state
                state = (c, 1)
        # end state
        if state[1] == 1:
            chars[cursor] = state[0]
            cursor += 1
        else:
            chars[cursor] = state[0]
            nlen = len(str(state[1]))
            chars[cursor+1:cursor+nlen+1] = str(state[1])
            cursor += 1 + nlen
        return cursor

class Solution:
    def compress(self, chars: List[str]) -> int:
        if not chars:
            return 0
        state = (None, 0)  # char, tally
        s = ''
        # start state machine
        for (i, c) in enumerate(chars):
            if state[0] is None:
                state = (c, 1)
            elif state[0] == c:
                state = (state[0], state[1] + 1)
            else:
                # character changed
                s += state[0] + (str(state[1]) if state[1] > 1 else '')
                state = (c, 1)
        # wrap up end state
        s += state[0] + (str(state[1]) if state[1] > 1 else '')
        chars[:] = list(s)
        return len(chars)
