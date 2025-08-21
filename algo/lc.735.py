class Solution:
    def addnum(self, stack: List[int], num: int):
        if len(stack) == 0:
            stack.append(num)
        elif num > 0:
            stack.append(num)
        elif stack[-1] < 0:
            stack.append(num)
        else:
            while len(stack) > 0:
                if stack[-1] > 0 and num < 0:
                    # eliminate
                    if stack[-1] > -num:
                        return
                    elif stack[-1] == -num:
                        stack.pop(-1)
                        return
                    else: # stack[-1] < -num
                        stack.pop(-1)
                else:
                    stack.append(num)
                    return
            # eliminated until stack empty
            stack.append(num)

    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack = []
        # push the rest
        for a in asteroids:
            self.addnum(stack, a)
            #print(stack)
        return stack
