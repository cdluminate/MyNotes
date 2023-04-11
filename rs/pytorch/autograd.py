
'''
http://pytorch.org/docs/master/notes/autograd.html
'''

import torch
from torch.autograd import Variable

# variable's requires_grad flag

x = Variable(torch.randn(5,5))
y = Variable(torch.randn(5,5))
z = Variable(torch.randn(5,5), requires_grad=True)
a = x+y
a.requires_grad
b = a+z
b.requires_grad

# TODO: variables's volatile flag

# supporting in-place operations in autograd is a hard matter.
