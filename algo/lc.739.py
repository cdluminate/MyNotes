class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        days = [0 for _ in temperatures]
        stack = []
        for (i, t) in enumerate(temperatures):
            if not stack:
                stack.append((i, t))
            elif stack[-1][-1] >= t:
                # not increasing
                stack.append((i, t))
            else:
                # increased
                while stack and stack[-1][-1] < t:
                    top = stack.pop(-1)
                    days[top[0]] = i - top[0]
                stack.append((i, t))
        return days

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        results = []
        for i in range(len(temperatures)):
            for j in range(i, len(temperatures)):
                if i == j: continue
                ti = temperatures[i]
                tj = temperatures[j]
                if ti < tj:
                    results.append(j-i)
                    break
            if len(results) <= i:
                results.append(0)
        return results

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        results = []
        stack = []
        for t in temperatures:
            if not stack or stack[-1] >= t:
                # not increasing, keep it
                stack.append(t)
            else:
                # increased. flush the stack.
                while stack:
                    results.append(len(stack))
                    stack.pop(-1)
                # reset the stack
                stack = [t]
        while len(results) != len(temperatures):
            results.append(0)
        return results
