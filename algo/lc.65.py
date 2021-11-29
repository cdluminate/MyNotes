#class Solution(object):
#    def isNumber(self, s):
#        """
#        :type s: str
#        :rtype: bool
#        """
#        if s == '': return False
#        if s.strip() == '.': return False
#        # define the Deterministic Finite Automata
#        dfa = [  # DFA init: q0, valid: q2,q4,q7,q8
#            {'blank':0, 'sign':1, 'digit':2, 'dot':3},  # q0
#            {'digit':2, 'dot':3},  # q1
#            {'digit':2, 'dot':3, 'e':5, 'blank':8},  # q2
#            {'digit':4, 'e':5, 'blank':8},  # q3
#            {'digit':4, 'e':5, 'blank':8},  # q4
#            {'digit':7, 'sign':6},  # q5
#            {'digit':7},  # q6
#            {'blank':8, 'digit':7},  # q7
#            {'blank':8},  # q8
#        ]
#        state = 0
#        # run the automata
#        for char in s:
#            #print(' * cursor char ', char, 'state', state)
#            # determine the type
#            if char.isnumeric():
#                char_t = 'digit'
#            elif char == '.':
#                char_t = 'dot'
#            elif char.isspace():
#                char_t = 'blank'
#            elif char == '+' or char == '-':
#                char_t = 'sign'
#            elif char == 'e':
#                char_t = 'e'
#            else:
#                return False
#            #print(' * cursor char is', char_t)
#            # is the type valid at current state?
#            if char_t not in dfa[state].keys():
#                #print(' * invalid convertion')
#                return False
#            # go to next state
#            state = dfa[state][char_t]
#            #print(' * goto', state)
#        # is the final state of automata valid?
#        if state not in [2,3,4,7,8]:
#            return False
#        return True
# Wrong answer

class Solution(object):
    def isNumber(self, s):
        """
        :type s: str
        :rtype: bool
        """
        #define a DFA
        state = [{}, 
              {'blank': 1, 'sign': 2, 'digit':3, '.':4}, 
              {'digit':3, '.':4},
              {'digit':3, '.':5, 'e':6, 'blank':9},
              {'digit':5},
              {'digit':5, 'e':6, 'blank':9},
              {'sign':7, 'digit':8},
              {'digit':8},
              {'digit':8, 'blank':9},
              {'blank':9}]
        currentState = 1
        for c in s:
            if c >= '0' and c <= '9':
                c = 'digit'
            if c == ' ':
                c = 'blank'
            if c in ['+', '-']:
                c = 'sign'
            if c not in state[currentState].keys():
                return False
            currentState = state[currentState][c]
        if currentState not in [3,5,8,9]:
            return False
        return True

if __name__ == '__main__':
    s = Solution()
    tests = [
            ('', False),
            ('3', True),
            ('-3', True),
            ('3.0', True),
            ('3.', True),
            ('3e1', True),
            ('3.0e1', True),
            ('3e+1', True),
            ('3e', False),
            ('+3.0e-1', True),
            ]
    for pair in tests:
        print(s.isNumber(pair[0]), pair[1])


