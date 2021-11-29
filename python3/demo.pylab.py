import numpy as np
import pylab

data = np.random.rand(50, 50)
pylab.pcolor(data) # pseudocolor plot of 2D array
pylab.colorbar()
#pylab.show()
pylab.savefig('x.svg')

# pylab.pcolormesh is an alternative to pylab.pcolor, but is faster!
