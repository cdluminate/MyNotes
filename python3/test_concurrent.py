from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import math
import random

x = [random.random() for _ in range(100)]

#with ProcessPoolExecutor() as executor:
with ThreadPoolExecutor() as executor:
    y = list(executor.map(math.cos, x))

print(y)
