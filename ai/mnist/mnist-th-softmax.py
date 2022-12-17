# http://pytorch.org/tutorials/
# http://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html
# https://github.com/pytorch/examples/blob/master/mnist/main.py

import sys
import os
os.putenv('OPENBLAS_NUM_THREADS', '4')

import torch as th
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
print('-> Using TH', th.__version__)
th.set_default_tensor_type('torch.DoubleTensor')

from dataloader import DataLoader
dataloader = DataLoader()

### Model ###
class Net(th.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = th.nn.Linear(784, 10) # affine operation
    def forward(self, x):
        x = self.fc1(x)
        x = F.log_softmax(x)
        return x

net = Net()
print(net)
crit = th.nn.NLLLoss() #th.nn.CrossEntropyLoss()
optimizer = th.optim.Adam(net.parameters(), lr=1e-2)

### Train
def transform(images, labels):
    images = images / 255.
    images = Variable(th.from_numpy(images.astype(np.double)), requires_grad=False)
    labels = Variable(th.from_numpy(labels.reshape(-1).astype(np.long)), requires_grad=False)
    return images, labels

for i in range(1000+1):
    # read data
    images, labels = dataloader.getBatch('train', 64)
    images, labels = transform(images, labels)

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
                'Accu {:.2f}|'.format(correct / total))

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
    predictions += [ pred[i][0] for i in range(len(pred)) ]
    print('.', end=''); sys.stdout.flush()
print(' -> prediction size ', len(predictions))
for i,l in enumerate(predictions):
    csvcontent += [ [str(i+1), str(l)] ]
with open('mnist-th-convnet.pred.csv', 'w+') as f:
    for line in csvcontent:
        f.write(','.join(line)+'\n')
print('-> done')
