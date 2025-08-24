class Solution:

    def isGood(self, intervals: List[List[int]]) -> bool:
        if not intervals:
            return True
        # mainatin segments
        segments = []
        traverse = list(intervals)
        while traverse:
            item = traverse.pop()
            #print('traverse>', traverse)
            # test each segment
            for (i, j) in segments:
                # overlap: one side of item is in segment
                if i < item[0] < j or i < item[1] < j:
                    #print('item>', item, 'is bad for', segments)
                    return False
                # item in segment
                elif i <= item[0] and item[1] <= j:
                    return False
                # segment in item
                elif item[0] <= i and j <= item[1]:
                    return False
            # passed all test, append item in segment
            segments.append(item)
            #print('segm>', segments)
        return True

    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        self.result = 0
        def dfs(state):
            if self.isGood(state):
                #print('>', state, 'is good')
                self.result = max(self.result, len(state))
            else:
                #print('>', state, 'is bad')
                # strike out one item
                for i in range(len(state)):
                    copy = list(state)
                    copy.pop(i)
                    dfs(copy)
        dfs(intervals)
        #print('debug>', self.result)
        return len(intervals) - self.result
