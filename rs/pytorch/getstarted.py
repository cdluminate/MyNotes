#!/usr/bin/env python3

'''
http://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html
'''

from __future__ import print_function
import torch as th
from torch.autograd import Variable
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

'''
http://pytorch.org/tutorials/beginner/blitz/tensor_tutorial.html
'''
print('------------------------------------------------')

# tensors

x = th.Tensor(5,3)
print(x)

x = th.rand(5,3)
print(x, x.size())

# operations

y = th.rand(5,3)
print(x+y)

print(th.add(x, y))

res = th.Tensor(5,3)
th.add(x, y, out=res)
print(res)

y.add_(x) # inplace, will change y
print(y)

print(x[:, 1])

# numpy bridge

a = th.ones(5)
print(a)

b = a.numpy()
print(b)

a.add_(1)
print(a, b) # both changed

a = np.ones(5)
b = th.from_numpy(a)
np.add(a, 1, out=a)
print(a, b) # both changed

# cuda tensor
# let us run this cell only if CUDA is available
if th.cuda.is_available():
    x = x.cuda()
    y = y.cuda()
    x + y

'''
http://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html

torch.autograd.Variable
  .data # raw tensor
  .grad # gradient accumulated here

torch.autograd.Function
'''
print('---------------------------------------------')

# variable

x = Variable(th.ones(2,2), requires_grad=True)
print(x)
y = x+2
print(y)
print(y.creator)

z = y*y*3
out = z.mean()
print(z, out)

# gradient

out.backward()
print(x.grad)

x = Variable(th.randn(3), requires_grad=True)
y = x*2
while y.data.norm() < 1000:
    y = y*2
print(y)

gradients = th.FloatTensor([0.1, 1.0, 0.0001])
y.backward(gradients)
print(x.grad)

'''
http://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html
'''

class Net(th.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = th.nn.Conv2d(1, 6, 5) # input channel, 6 out channel, 5x5 conv
        self.conv2 = th.nn.Conv2d(6, 16, 5)
        self.fc1 = th.nn.Linear(16*5*5, 120) # affine operation
        self.fc2 = th.nn.Linear(120, 84)
        self.fc3 = th.nn.Linear(84, 10)
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2,2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    def num_flat_features(self, x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

net = Net()
print(net)

params = list(net.parameters())
print(len(params))
print(params[0].size())

print('-> forward 1 image')
images = Variable(th.randn(1, 1, 32, 32))
out = net(images)
print(out)

net.zero_grad()
out.backward(th.randn(1, 10))

# torch.nn only supports mini-batchs, not a single sample
#images = Variable(th.randn(5, 1, 32, 32)) # a batch
#out = net(images)
#print(out)

out = net(images)
label = Variable(th.arange(1, 11))
crit = th.nn.MSELoss()
loss = crit(out, label)
print(loss)

print(loss.creator)
print(loss.creator.previous_functions[0][0]) # linear
print(loss.creator.previous_functions[0][0].previous_functions[0][0]) # relu

net.zero_grad()
print('conv1.bias.grad before backward')
print(net.conv1.bias.grad)
loss.backward()
print('conv1.bias.grad after backward')
print(net.conv1.bias.grad)

#learning_rate = 0.01
#for f in net.parameters():
#    f.data.sub_(f.grad.data * learning_rate)
optimizer = optim.SGD(net.parameters(), lr=0.01)

# in your training loop:
optimizer.zero_grad()
output = net(images)
loss = crit(output, label)
loss.backward()
optimizer.step() # update
