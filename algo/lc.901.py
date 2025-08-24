class StockSpanner:

    def __init__(self):
        self.day = -1
        self.stack = []

    def next(self, price: int) -> int:
        self.day += 1
        if not self.stack:
            self.stack.append([self.day, price])
            print('empty stack>', self.stack)
            return 1
        elif self.stack[-1][-1] <= price:
            # the price increased. continue the span
            top = None
            while self.stack and self.stack[-1][-1] <= price:
                top = self.stack.pop(-1)
            if self.stack:
                days = self.day - self.stack[-1][0]
            else:
                days = self.day + 1
            self.stack.append([self.day, price])
            print('continue span>', self.stack)
            return days
        else:
            # the span is broken
            days = self.day - self.stack[-1][0]
            self.stack.append([self.day, price])
            print('span broken>', self.stack)
            return days
            

        


# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)
