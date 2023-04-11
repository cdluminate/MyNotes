#!/usr/bin/env python3

'''
http://pytorch.org/tutorials/beginner/pytorch_with_examples.html
'''
import sys
import os
import time
import random

import torch as th
dtype = th.FloatTensor

print('Using TH', th.__version__)

# batchsize, input dim, hidden dim, output dim
N, Din, Dhid, Dout = 64, 1000, 100, 10

# create random input data
x = th.randn(N, Din).type(dtype)
y = th.randn(N, Dout).type(dtype)

# init weight
w1 = th.randn(Din, Dhid).type(dtype)
w2 = th.randn(Dhid, Dout).type(dtype)

lr = 1e-6
for it in range(500):
  # forward pass
  h = x.mm(w1)
  h_ = h.clamp(min=0) # relu
  y_ = h_.mm(w2)
  
  # loss, MSE
  loss = (y_ - y).pow(2).sum()
  print('-> iter {:5d} |'.format(it), 'loss {:10.2f}'.format(loss))

  # backward
  grad_y_ = 2.0 * (y_ - y)
  grad_w2 = h_.t().mm(grad_y_)
  grad_h_ = grad_y_.mm(w2.t())
  grad_h  = grad_h_.clone()
  grad_h[h<0] = 0
  grad_w1 = x.t().mm(grad_h)

  # update
  w1 -= lr * grad_w1
  w2 -= lr * grad_w2

#time.sleep(2)

print('Autograd')

from torch.autograd import Variable

xx = Variable(th.randn(N, Din).type(dtype), requires_grad=False)
yy = Variable(th.randn(N, Dout).type(dtype), requires_grad=False)

ww1 = Variable(th.randn(Din, Dhid).type(dtype), requires_grad=True)
ww2 = Variable(th.randn(Dhid, Dout).type(dtype), requires_grad=True)

lr = 1e-6
for it in range(500):
  # forward pass
  yy_ = xx.mm(ww1).clamp(min=0).mm(ww2)
  # loss
  loss = (yy_ - yy).pow(2).sum()
  print('-> iter {:5d} |'.format(it), 'loss {:10.2f}'.format(loss.data[0]))
  # backward
  loss.backward()
  # update
  ww1.data -= lr * ww1.grad.data
  ww2.data -= lr * ww2.grad.data
  # zero grad
  ww1.grad.data.zero_()
  ww2.grad.data.zero_()

print('MyReLU')

class MyReLU(th.autograd.Function):
  '''
  Custom autograd function, we need to implement forward and backward methods.
  '''
  def forward(self, input):
    self.save_for_backward(input)
    return input.clamp(min=0)
  def backward(self, grad_output):
    input, = self.saved_tensors
    grad_input = grad_output.clone()
    grad_input[input < 0] = 0
    return grad_input

xxx = Variable(th.randn(N, Din).type(dtype), requires_grad=False)
yyy = Variable(th.randn(N, Dout).type(dtype), requires_grad=False)

www1 = Variable(th.randn(Din, Dhid).type(dtype), requires_grad=True)
www2 = Variable(th.randn(Dhid, Dout).type(dtype), requires_grad=True)

for it in range(500):
  # instance
  relu = MyReLU()
  # forward
  yyy_ = relu(xxx.mm(www1)).mm(www2)
  # loss
  loss = (yyy_ - yyy).pow(2).sum()
  print('-> iter {:5d} |'.format(it), 'loss {:10.2f}'.format(loss.data[0]))
  # backward
  loss.backward()
  # update
  www1.data -= lr * www1.grad.data
  www2.data -= lr * www2.grad.data
  # zero grad
  www1.grad.data.zero_()
  www2.grad.data.zero_()

'''
The biggest difference between the two is that TensorFlow’s computational
graphs are static and PyTorch uses dynamic computational graphs.
''' 

print('Pytorch: nn')

model = th.nn.Sequential(
  th.nn.Linear(Din, Dhid),
  th.nn.ReLU(),
  th.nn.Linear(Dhid, Dout),
)
crit = th.nn.MSELoss(size_average=False)

lr = 1e-4
for it in range(500):
  # forward
  y_ = model(xx)
  # loss
  loss = crit(y_, yy)
  print('-> iter {:5d} |'.format(it), 'loss {:10.2f}'.format(loss.data[0]))
  # zero grad
  model.zero_grad()
  # backward
  loss.backward()
  # update
  for param in model.parameters():
    param.data -= lr * param.grad.data
  
print('Pytorch: optim')

model2 = th.nn.Sequential(
  th.nn.Linear(Din, Dhid),
  th.nn.ReLU(),
  th.nn.Linear(Dhid, Dout),
)
crit = th.nn.MSELoss(size_average=False)
optimizer = th.optim.Adam(model2.parameters(), lr=1e-4)

for it in range(500):
  # forward
  y_ = model2(xx)
  # loss
  loss = crit(y_, yy)
  print('-> iter {:5d} |'.format(it), 'loss {:10.2f}'.format(loss.data[0]))
  # zero grad
  optimizer.zero_grad()
  # backward
  loss.backward()
  # update
  optimizer.step()

print('Pytorch : custom nn module')

class TwoLayerNet(th.nn.Module):
  def __init__(self, Din, Dhid, Dout):
    super(TwoLayerNet, self).__init__()
    self.l1 = th.nn.Linear(Din, Dhid)
    self.l2 = th.nn.Linear(Dhid, Dout)
  def forward(self, x):
    h_ = self.l1(x).clamp(min=0)
    y_ = self.l2(h_)
    return y_

model3 = TwoLayerNet(Din, Dhid, Dout)
crit = th.nn.MSELoss(size_average=False)
optimizer = th.optim.SGD(model3.parameters(), lr=1e-4)

for it in range(500):
  y_ = model3(xx)
  loss = crit(y_, yy)
  print('-> iter {:5d} |'.format(it), 'loss {:10.2f}'.format(loss.data[0]))
  optimizer.zero_grad()
  loss.backward()
  optimizer.step()

print('Pytorch: control flow + weight sharing')

class DynNet(th.nn.Module):
  def __init__(self, Din, Dhid, Dout):
    super(DynNet, self).__init__()
    self.inL = th.nn.Linear(Din, Dhid)
    self.midL = th.nn.Linear(Dhid, Dhid)
    self.outL = th.nn.Linear(Dhid, Dout)
  def forward(self, x):
    h_ = self.inL(x).clamp(min=0)
    for _ in range(random.randint(0,3)):
      h_ = self.midL(h_).clamp(min=0)
    y_ = self.outL(h_)
    return y_

model4 = DynNet(Din, Dhid, Dout)
crit = th.nn.MSELoss(size_average=False)
optimizer = th.optim.SGD(model4.parameters(), lr=1e-4, momentum=0.9)
for it in range(500):
  y_ = model4(xx)
  loss = crit(y_, yy)
  print('-> iter {:5d} |'.format(it), 'loss {:10.2f}'.format(loss.data[0]))
  optimizer.zero_grad()
  loss.backward()
  optimizer.step()

print('done')

