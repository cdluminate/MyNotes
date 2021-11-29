# https://matplotlib.org/gallery/animation/animation_demo.html#sphx-glr-gallery-animation-animation-demo-py
import pylab as lab
import numpy as np
import random
import time

fig, ax = lab.subplots()
fig2, ax2 = lab.subplots(2, 1)
data = np.random.random((50, 50, 50))

for i in range(len(data)):
    ax.cla()
    ax.imshow(data[i])
    ax.set_title(f'frame {i}')

    ax2[0].cla()
    ax2[0].imshow(1- data[i])
    ax2[0].set_title(f'ax2 frame {i}')

    ax2[1].cla()
    ax2[1].plot(np.random.random(50))
    ax2[1].set_title('hello')

    lab.pause(0.1)
