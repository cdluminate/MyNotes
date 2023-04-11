# http://pytorch.org/tutorials/
# http://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html
# https://github.com/pytorch/examples/blob/master/mnist/main.py

import sys
import os
import time

import torch as th
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
print('-> Using TH', th.__version__)

perf_tm = {}
perf_getdiff = lambda d: d['end'] - d['start']

### Setting up *_NUM_THREADS env variable ###
# https://discuss.pytorch.org/t/how-long-does-it-take-to-train-the-network-in-the-cifar-10-tutorial/1929/8
# A large number of CPU cores may be a reason of slowdown. Use a small number of threads.
X_THNUM = '4'
os.putenv('OPENBLAS_NUM_THREADS', X_THNUM)
os.putenv('OMP_NUM_THREADS', X_THNUM)
os.putenv('MKL_NUM_THREADS', X_THNUM)

USE_GPU = True if len(sys.argv)>1 else False # Append any argument to command line to toggle GPU mode
USE_GPU = USE_GPU if th.cuda.is_available() else False
print('-> USE_GPU: {}'.format(USE_GPU))

th.manual_seed(1)
if not USE_GPU:
    th.set_default_tensor_type('torch.DoubleTensor')
else:
    th.set_default_tensor_type('torch.cuda.DoubleTensor')
    th.cuda.manual_seed(1)

from dataloader import DataLoader
dataloader = DataLoader()

### Model ###
class Net(th.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = th.nn.Conv2d(1, 6, 5) # input channel, 6 out channel, 5x5 conv
        self.bn1 = th.nn.BatchNorm2d(6)
        self.conv2 = th.nn.Conv2d(6, 16, 5)
        self.bn2 = th.nn.BatchNorm2d(16)
        self.fc3 = th.nn.Linear(16*4*4, 120) # affine operation
        self.bn3 = th.nn.BatchNorm2d(120)
        self.fc4 = th.nn.Linear(120, 84)
        self.bn4 = th.nn.BatchNorm1d(84)
        self.drop4 = th.nn.Dropout(p=0.2)
        self.fc5 = th.nn.Linear(84, 10)
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.bn1(self.conv1(x))), (2,2))
        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.bn3(self.fc3(x)))
        x = F.relu(self.bn4(self.fc4(x)))
        x = self.drop4(x)
        x = self.fc5(x)
        return x
    def num_flat_features(self, x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

net = Net() if not USE_GPU else Net().cuda()
print(net)
crit = th.nn.CrossEntropyLoss()
optimizer = th.optim.Adam(net.parameters(), lr=1e-2)

### Train
def transform(images, labels):
    images = images.reshape(-1, 1, 28, 28) / 255.
    images = Variable(th.from_numpy(images.astype(np.double)), requires_grad=False)
    labels = Variable(th.from_numpy(labels.reshape(-1).astype(np.long)), requires_grad=False)
    if USE_GPU: images, labels = images.cuda(), labels.cuda() 
    return images, labels

#for i in range(100+1):
perf_tm['start'] = time.time()
for i in range(2500+1):
    # read data
    images, labels = dataloader.getBatch('train', 64)
    images, labels = transform(images, labels)

    # half the learning rate @ iter 500
    if i==500 or i==1000 or i==2000:
        print('-> half the learning rate')
        for param_group in optimizer.param_groups:
            param_group['lr'] *= 0.5
            print(param_group['lr'])

    # train
    net.train()
    out = net(images)
    loss = crit(out, labels)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    pred = out.data.max(1)[1]
    correct = pred.eq(labels.data).cpu().sum()
    print('-> Iter {:5d} |'.format(i), 'loss {:7.3f} |'.format(loss.data[0]),
            'Bch Train Accu {:.2f}'.format(correct / out.size()[0]))

    # val
    if i%100==0:
        print('-> TEST @ {} |'.format(i), end='')
        net.eval()
        correct = 0
        total = 0
        lossaccum = 0
        dataloader.reset('val')
        for j in range(dataloader.itersInEpoch('val', 100)):
            images, labels = dataloader.getBatch('val', 100)
            images, labels = transform(images, labels)
            out = net(images)
            loss = crit(out, labels)
            pred = out.data.max(1)[1]
            correct += pred.eq(labels.data).cpu().sum()
            total += 100
            lossaccum += loss.data[0]
            print('.', end=''); sys.stdout.flush()
        print('|')
        print('-> TEST @ {} |'.format(i),
                'Loss {:7.3f} |'.format(lossaccum),
                'Accu {:.5f}|'.format(correct / total))

### Make prediction and export to csv
print('-> making prediction')
net.eval()
dataloader.reset('test')
csvcontent = [ ['ImageID', 'Label'] ]
predictions = []
for i in range(dataloader.itersInEpoch('test', 100)):
    images, labels = dataloader.getBatch('test', 100)
    images, labels = transform(images, labels)
    out = net(images)
    pred = out.data.max(1)[1]
    #predictions += [ pred[i][0] for i in range(len(pred)) ]
    predictions += [ pred[i] for i in range(len(pred)) ] # pytorch 0.2.0
    print('.', end=''); sys.stdout.flush()
print(' -> prediction size ', len(predictions))
for i,l in enumerate(predictions):
    csvcontent += [ [str(i+1), str(l)] ]
with open('mnist-th-convnet.pred.csv', 'w+') as f:
    for line in csvcontent:
        f.write(','.join(line)+'\n')
perf_tm['end'] = time.time()
print('-> done, time elapsed', perf_getdiff(perf_tm))

'''
time:

    2500 iters
     + 6900K CPU: 4-Threads: 53.69774103164673 s
     + 6900K + TitanX Pascal / CUDA 8.0 GPU: 13.732074737548828 s
     + TitanX Pascal / fp32 : 9.233038902282715 s
     + 2687W CPU: 4-Threads: ? s
     + 2520M CPU: 4-Threads: 99.17602920532227 s

    -> GPU is 3.9x faster than 6900K CPU.
    -> 6900K is 1.86x faster than 2520M.

cuda:

    1. pytorch pin_memory: http://pytorch.org/docs/master/notes/cuda.html
       see how DataLoader "pin" the memory. (page-locked memory)

further:

    https://www.kaggle.com/c/digit-recognizer/discussion/4045

    1. Synthesizing more training data using image processing libraries.
       e.g. rotate left, rotate right, zoom, stretch horizontally and
       vertivally, elastic deformations
    2. reduce overfitting using concepts of early convergence and dropout.
'''
