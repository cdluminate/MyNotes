import tqdm
import time

for i in tqdm.tqdm(range(200)):
    time.sleep(0.01)

for i in tqdm.trange(200):
    time.sleep(0.01)
