#!/usr/bin/env python3
'''
Informal repro of CV16 - ORCNN : MR-CNN
Unofficial and Modified implementation of Ordinal Regression With Multiple Output CNN for Age Estimation (CVPR2016).
'''
import sys
import os
import time
from collections import OrderedDict, deque
import random
import argparse
import json
import math
from PIL import Image

import numpy as np
import torch as th
import torch.nn.init
import torch.nn.functional as F
from torch.autograd import Variable

from dataloader import DataLoader

### CONFIGURE ###
argparser = argparse.ArgumentParser()
argparser.add_argument('-g', '--gpu', action='store_true',
                       help='use GPU/CUDA insteaf of CPU')
argparser.add_argument('-d', '--double', action='store_true',
                       help='use fp64 instead of fp32')
argparser.add_argument('-m', '--maxiter', type=int, default=72000,
                       help='set maximum iterations of training',)
argparser.add_argument('-s', '--seed', type=int, default=1,
                       help='set manual seed')
argparser.add_argument('-n', '--numthreads', type=int, default=4,
                       help='set *_NUM_THREADS environment variable')
argparser.add_argument('-t', '--testevery', type=int, default=500,
                       help='set model evaluation interval')
argparser.add_argument('-o', '--decay0', type=int, default=975,
                       help='set the first iteration where the learning rate starts to decay')
argparser.add_argument('-T', '--decayT', type=int, default=1950,
                       help='set the learning rate decay period')
argparser.add_argument('-e', '--lr', type=float, default=1e-4,
                       help='set the initial learning rate')
argparser.add_argument('-b', '--batchsize', type=int, default=128,
                       help='set batch size for training')
argparser.add_argument('--testbatchsize', type=int, default=100,
                       help='set batch size for test')
args = argparser.parse_args()
print('=> Dump configuration')
print(json.dumps(vars(args), indent=2))

### ENVIRONMENT ###
os.putenv('OPENBLAS_NUM_THREADS', str(args.numthreads))
os.putenv('OMP_NUM_THREADS', str(args.numthreads))
os.putenv('MKL_NUM_THREADS', str(args.numthreads))

### Misc
def barX(colorcode):
    return lambda x,xmax,width: print('{:>4.0%}'.format(x/xmax)+\
        '|'+'\x1b[{};1m'.format(colorcode)+'*'*round(width*x/xmax)+\
        ' '*round(width-width*x/xmax)+'\x1b[;m'+'|')
# Tips : get terminal width like this -- os.get_terminal_size().columns-6
barG = barX('32') # Green for train Acc
barY = barX('33') # Yellow for train loss
barC = barX('36') # Cyan for test Acc
barR = barX('31') # Red for test loss

### TIMER SETUP ###
class Perf_TM(object):
    def __init__(self):
        self.d = {} # dict{'key': list[float]}
    def go(self, key):
        if key not in self.d.keys(): self.d[key] = []
        self.d[key].append(-time.time())
    def halt(self, key):
        self.d[key][-1] += time.time()
    def dump(self):
        s = dict(self.d)
        for key in s.keys():
            if len(s[key])>1:
                num_rec = len(s[key])
                s[key] = [sum(s[key])/num_rec, 'Average of the '+str(num_rec)+' records']
        print(json.dumps(s, indent=2))
perf_tm = Perf_TM()

### SETUP Recorder, for loss curve and etc.
class Perf_ML(dict):
    def go(self, name, it, value):
        if name not in self.keys():
            self[name] = []
        self[name].append((it, value))
    def dump(self, name=None):
        for k,v in self['test/loss']:
            barR(v, self['test/loss'][0][1], 100)
        for k,v in self['test/mae']:
            barC(v, self['test/mae'][0][1], 100)
perf_ml = Perf_ML()

### TORCH SETUP ###
print('-> Using PyTorch', th.__version__)
th.manual_seed(args.seed)
if args.gpu: th.cuda.manual_seed(args.seed)
X_TENSOR = ''
if not args.gpu:
    X_TENSOR = 'torch.DoubleTensor' if args.double else 'torch.FloatTensor'
else:
    X_TENSOR = 'torch.cuda.DoubleTensor' if args.double else 'torch.cuda.FloatTensor'
    #th.set_default_tensor_type('torch.cuda.HalfTensor') # Bad Stability
th.set_default_tensor_type(X_TENSOR)

### DataLoader ###
dataloader = DataLoader()

### Model ###
class Model(th.nn.Module):
    '''
    60x60 input image cropped from 64x64 image
    batchsize is 128
    label should be shifted by -16
    '''
    def __init__(self):
        super(Model, self).__init__()
        self.SEQ1 = th.nn.Sequential(OrderedDict([
          # 128x3x60x60
          ('conv1', th.nn.Conv2d(3, 20, 5, stride=1, padding=0)),
          # 128x20x56x56
#          ('bn1',   th.nn.BatchNorm2d(20)),
          ('relu1', th.nn.ReLU()),
          ('norm1', th.nn.CrossMapLRN2d(9, alpha=0.001, beta=0.75)),
          ('pool1', th.nn.MaxPool2d(3, stride=2, padding=1)),
          # 128x20x28x28

          ('conv2', th.nn.Conv2d(20, 40, 7, stride=1, padding=0)),
          # 128x40x22x22
#          ('bn2',   th.nn.BatchNorm2d(40)),
          ('relu2', th.nn.ReLU()),
          ('norm2', th.nn.CrossMapLRN2d(9, alpha=0.001, beta=0.75)),
          ('pool2', th.nn.MaxPool2d(3, stride=2, padding=1)),
          # 128x40x11x11

          ('conv3', th.nn.Conv2d(40, 80, 11, stride=1, padding=0)),
          # 128x80x1x1
#          ('bn3',   th.nn.BatchNorm2d(80)),
          ('relu3', th.nn.ReLU()),
          ('norm3', th.nn.CrossMapLRN2d(9, alpha=0.001, beta=0.75)),

        ]))
        th.nn.init.normal(self.SEQ1.conv1.weight, mean=0, std=0.01)
        th.nn.init.constant(self.SEQ1.conv1.bias, 0.05)
        th.nn.init.normal(self.SEQ1.conv2.weight, mean=0, std=0.01)
        th.nn.init.constant(self.SEQ1.conv2.bias, 0.05)
        th.nn.init.normal(self.SEQ1.conv3.weight, mean=0, std=0.01)
        th.nn.init.constant(self.SEQ1.conv3.bias, 0.05)

        self.SEQ2 = th.nn.Sequential(OrderedDict([
          # 128x80
          ('fc4',   th.nn.Linear(80, 80)),
          # 128x80
          ('bn4',   th.nn.BatchNorm1d(80)),
          ('relu4', th.nn.ReLU()),

#          ('drop5', th.nn.Dropout(0.2)),
          ('fc5',   th.nn.Linear(80, 1)),
          # 128x1
        ]))
        th.nn.init.normal(self.SEQ2.fc4.weight, mean=0, std=0.005)
        th.nn.init.constant(self.SEQ2.fc4.bias, 0.05)
        th.nn.init.normal(self.SEQ2.fc5.weight, mean=0, std=0.005)
        th.nn.init.constant(self.SEQ2.fc5.bias, 0.05)

        self.DUMPSHAPE = False
    def forward(self, x):
        if not self.DUMPSHAPE:
            def psize(size):
                msg = ''
                for x in size: msg += '{} '.format(x)
                prod = 1
                for x in size[1:]: prod *= x
                msg += '({} x {})'.format(size[0], prod)
                return msg
            def dumpshape(module, x):
                for name, m in list(module.named_modules())[1:]:
                    print('*> pre ', name.center(16),
                          'SHAPE', psize(x.size()).center(32))
                    x = m(x)
                    print('*> post', name.center(16),
                          'SHAPE', psize(x.size()).center(32))
                return x
            x = dumpshape(self.SEQ1, x)
            x = x.view(-1, 80)
            x = dumpshape(self.SEQ2, x)
            self.DUMPSHAPE = True
        else:
            x = self.SEQ1(x)
            x = x.view(-1, 80)
            x = self.SEQ2(x)
        return x

### Create Instances
net = Model() if not args.gpu else Model().cuda()
if not args.double: net = net.float()
print(net)
crit = th.nn.MSELoss() # Caffe:EuclideanLoss
optimizer = th.optim.SGD(net.parameters(), lr=args.lr, momentum=0.9, weight_decay=5e-4)

### Data Transformation
image_mean = np.load('morph2.mean64x64.npz')['arr_0']
image_mean[[0,2],:,:] = image_mean[[2,0],:,:]
def transform(images, labels, evaluate=False):
    # cropping
    if evaluate==True:
        xoff, yoff = 2, 2
    else:
        xoff, yoff = random.randint(0,4), random.randint(0,4)
    # mean, scale and shift
    images = (images - image_mean)[:,:,yoff:yoff+60, xoff:xoff+60]/ 255.
    labels = labels - 16.
    # mirroring while training
    if evaluate==False and random.choice((True,False)):
        images = np.flip(images, 3)
    images = Variable(th.from_numpy(images.astype(np.double)), requires_grad=False)
    labels = Variable(th.from_numpy(labels.reshape(-1, 1).astype(np.double)), requires_grad=False)
    if args.gpu: images, labels = images.cuda(), labels.cuda()
    if not args.double: images, labels = images.float(), labels.float()
    return images, labels

### Evaluation on Validation set
def evaluate(i, net, dataloader):
    print('-> EVAL @ {} |'.format(i), end='')
    net.eval()
    maeaccum = 0
    lossaccum = 0
    total = 0
    dataloader.reset('val')
    for j in range(dataloader.itersInEpoch('val', args.testbatchsize)):
        images, labels = dataloader.getBatch('val', args.testbatchsize)
        images, labels = transform(images, labels, True)
        out = net(images)
        loss = crit(out, labels)

        maeaccum += th.Tensor(out.data).add(-labels.data).abs().sum()
        lossaccum += loss.data[0]
        total += args.testbatchsize
        print('.', end=''); sys.stdout.flush()

    mae = maeaccum / total
    loss = lossaccum / total
    print('|')
    print('-> TEST @ {} |'.format(i),
            'Loss {:7.3f} |'.format(loss),
            'MAE {:.5f}|'.format(mae))
    perf_ml.go('test/mae', i, mae)
    perf_ml.go('test/loss', i, lossaccum / total)
    barC(mae, perf_ml['test/mae'][0][1], 80)
    #barR(lossaccum, perf_ml['test/loss'][0][1], 80)

### Training
perf_tm.go('all')
smthmae = deque([], 17) # ~5% of trainset
for i in range(args.maxiter+1):
    # read data
    perf_tm.go('data/fetch')
    images, labels = dataloader.getBatch('train', args.batchsize)
    #images, labels = dataloader.Q.get()
    images, labels = transform(images, labels)
    perf_tm.halt('data/fetch')

    # decay the learning rate
    # inv: return base_lr * (1 + gamma * iter) ^ (- power)
    curlr = args.lr * (1 + 1e-4 * i)**(- 0.75)
    for param_group in optimizer.param_groups:
        param_group['lr'] = curlr

    # train
    perf_tm.go('train/flbu')
    net.train()
    out = net(images)
    loss = crit(out, labels)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    perf_tm.halt('train/flbu')

    mae = th.Tensor(out.data).add(-labels.data).abs().sum() / args.batchsize
    smthmae.append(mae)

    print('-> Iter {:5d} ({:<5d}/{:5d} Eph {:>3d} ) |'.format(i,
            (i+1)*args.batchsize % dataloader.max['train'],
            dataloader.max['train'],
            int((i+1)*args.batchsize / dataloader.max['train'])),
            'loss {:7.3f} |'.format(loss.data[0]),
            'Batch MAE {:.2f}'.format(mae),
            '(Smth {:.2f})'.format(sum(smthmae)/len(smthmae)))
    perf_ml.go('train/loss', i, loss.data[0])
    perf_ml.go('train/mae', i, mae)
    barG(mae, perf_ml['train/mae'][0][1], 80)
    barY(loss.data[0], perf_ml['train/loss'][0][1], 80)

    # test
    if i%args.testevery==0: evaluate(i, net, dataloader)

perf_tm.halt('all')
print('-> Complete. Time elapsed', perf_tm.d['all'])

print('=> Dump Summaries')
perf_tm.dump()
perf_ml.dump()

# Save the model
modelpath = '{}.iter{}.pth'.format(__file__, i)
print('=> Saving model to {}'.format(modelpath))
th.save(net, modelpath)
print('=> Reload and test')
net = th.load(modelpath)
evaluate('final', net, dataloader)

'''
Ref experiment
  Adam is not always better than SGD. Here SGD seems to perform much better. (lr)?
  The performance gets worse with all the BN layers enabled.
  BN makes the optimization slightly simpler.
Ref performance

  [morph2.cv16.wacv82.h5] | rotation due to swapaxes(0,2)
  MAE 3.6 24000
  MAE 3.26 72000
  MAE 3.4 bn4
  MAE best@3.15 bn4, 72000
  MAE best@3.13 bn4+drop0.2, 72000
  MAE best@3.16 bn4+no_norm, 72000

  [morph2.wacv82.cv16.norotation.h5]
  MAE bn4    -> TEST @ 42000 | Loss   0.166 | MAE 3.06694|
  MAE no-bn4 -> TEST @ 62500 | Loss   0.173 | MAE 3.14324|
  MAE bn1~bn3+no_affine bn4 adam -> TEST @ 72000 | Loss   0.166 | MAE 3.07891|
  MAE bn1~bn3+no_affine bn4 sgd  -> TEST @ 65000 | Loss   0.169 | MAE 3.08269|
'''

''' solver.prototxt e22_wacv
net: "net.prototxt"
# train.subset test2 has 10000 images
test_iter: 104
test_interval: 200
base_lr: 0.0001
lr_policy: "inv"
gamma: 0.0001
power: 0.75
stepsize: 100000
display: 1
max_iter: 24000
momentum: 0.9
weight_decay: 0.0005
snapshot: 500
snapshot_prefix: "cnnage"
solver_mode: CPU # -- Intel Xeon W3690
#debug_info: true
'''

''' net.prototxt e22_wacv
name: "data" mirror: true crop_size: 60 mean_file: "wacv8.mean" batch_size: 128
name: "data" mirror: false crop_size: 60 mean_file: "wacv2.mean" batch_size: 100
name: "power" bottom: "label" top: "labelp" power: 1.0 scale: 1.0 shift: -16.0

name: "conv1" num_output: 20 kernel_size: 5 stride: 1 pad: 0 weight_filler { type: "gaussian" std: 0.01 } bias_filler { type: "constant" value: 0.05 }
name: "relu1"
name: "norm1" type: "LRN" lrn_param { local_size: 9 alpha: 0.001 beta: 0.75 }
name: "pool1" type: "Pooling" pooling_param { pool: MAX kernel_size: 3 stride: 2 }

name: "conv2" num_output: 40 kernel_size: 7 stride: 1 pad: 0 weight_filler { type: "gaussian" std: 0.01 } bias_filler { type: "constant" value: 0.05 }
name: "relu2"
name: "norm2" type: "LRN" lrn_param { local_size: 9 alpha: 0.001 beta: 0.75 }
name: "pool2" type: "Pooling" pooling_param { pool: MAX kernel_size: 3 stride: 2 }

name: "conv3" num_output: 80 kernel_size: 11 stride: 1 pad: 0 weight_filler { type: "gaussian" std: 0.01 } bias_filler { type: "constant" value: 0.05 }
name: "relu3"
name: "norm3" type: "LRN" lrn_param { local_size: 9 alpha: 0.001 beta: 0.75 }

name: "fc4" type: "InnerProduct" num_output: 80 weight_filler { type: "gaussian" std: 0.005 } bias_filler { type: "constant" value: 0.05 }
name: "relu4"
name: "fc5" type: "InnerProduct" num_output: 1 weight_filler { type: "gaussian" std: 0.005 } bias_filler { type: "constant" value: 0.05 }

name: "loss" type: "EuclideanLoss"
name: "MAE" type: "MAE" bottom: "fc5" bottom: "labelp"

## append 1 Apr. 2016
layer { name: "dumpprediction" type: "Power" bottom: "fc5" top: "dumpprediction" }
layer { name: "dumplable" type: "Power" bottom: "labelp" top: "dumplabel" }
'''

'''
I0821 15:14:39.903503 26133 net.cpp:380] data -> data
I0821 15:14:39.903602 26133 net.cpp:129] Top shape: 128 3 60 60 (1382400)

I0821 15:14:39.903750 26133 net.cpp:380] label -> label
I0821 15:14:39.903837 26133 net.cpp:129] Top shape: 128 1 (128)

I0821 15:14:39.903944 26133 net.cpp:406] power <- label
I0821 15:14:39.903960 26133 net.cpp:380] power -> labelp
I0821 15:14:39.904016 26133 net.cpp:129] Top shape: 128 1 (128)

I0821 15:14:39.904075 26133 net.cpp:406] conv1 <- data
I0821 15:14:39.904093 26133 net.cpp:380] conv1 -> conv1
I0821 15:14:39.904253 26133 net.cpp:129] Top shape: 128 20 56 56 (8028160)

I0821 15:14:39.904321 26133 net.cpp:406] relu1 <- conv1
I0821 15:14:39.904336 26133 net.cpp:367] relu1 -> conv1 (in-place)
I0821 15:14:39.904367 26133 net.cpp:129] Top shape: 128 20 56 56 (8028160)

I0821 15:14:39.904420 26133 net.cpp:406] norm1 <- conv1
I0821 15:14:39.904435 26133 net.cpp:380] norm1 -> norm1
I0821 15:14:39.904471 26133 net.cpp:129] Top shape: 128 20 56 56 (8028160)

I0821 15:14:39.904528 26133 net.cpp:406] pool1 <- norm1
I0821 15:14:39.904544 26133 net.cpp:380] pool1 -> pool1
I0821 15:14:39.904580 26133 net.cpp:129] Top shape: 128 20 28 28 (2007040)

I0821 15:14:39.904635 26133 net.cpp:406] conv2 <- pool1
I0821 15:14:39.904651 26133 net.cpp:380] conv2 -> conv2
I0821 15:14:39.905395 26133 net.cpp:129] Top shape: 128 40 22 22 (2478080)

I0821 15:14:39.905454 26133 net.cpp:406] relu2 <- conv2
I0821 15:14:39.905469 26133 net.cpp:367] relu2 -> conv2 (in-place)
I0821 15:14:39.905500 26133 net.cpp:129] Top shape: 128 40 22 22 (2478080)

I0821 15:14:39.905552 26133 net.cpp:406] norm2 <- conv2
I0821 15:14:39.905567 26133 net.cpp:380] norm2 -> norm2
I0821 15:14:39.905601 26133 net.cpp:129] Top shape: 128 40 22 22 (2478080)

I0821 15:14:39.905652 26133 net.cpp:406] pool2 <- norm2
I0821 15:14:39.905668 26133 net.cpp:380] pool2 -> pool2
I0821 15:14:39.905704 26133 net.cpp:129] Top shape: 128 40 11 11 (619520)

I0821 15:14:39.905758 26133 net.cpp:406] conv3 <- pool2
I0821 15:14:39.905774 26133 net.cpp:380] conv3 -> conv3
I0821 15:14:39.914450 26133 net.cpp:129] Top shape: 128 80 1 1 (10240)

I0821 15:14:39.914613 26133 net.cpp:406] relu3 <- conv3
I0821 15:14:39.914654 26133 net.cpp:367] relu3 -> conv3 (in-place)
I0821 15:14:39.914734 26133 net.cpp:129] Top shape: 128 80 1 1 (10240)

I0821 15:14:39.914880 26133 net.cpp:406] norm3 <- conv3
I0821 15:14:39.914921 26133 net.cpp:380] norm3 -> norm3
I0821 15:14:39.915004 26133 net.cpp:129] Top shape: 128 80 1 1 (10240)

I0821 15:14:39.915148 26133 net.cpp:406] fc4 <- norm3
I0821 15:14:39.915189 26133 net.cpp:380] fc4 -> fc4
I0821 15:14:39.915402 26133 net.cpp:129] Top shape: 128 80 (10240)

I0821 15:14:39.915550 26133 net.cpp:406] relu4 <- fc4
I0821 15:14:39.915588 26133 net.cpp:367] relu4 -> fc4 (in-place)
I0821 15:14:39.915668 26133 net.cpp:129] Top shape: 128 80 (10240)

I0821 15:14:39.915812 26133 net.cpp:406] fc5 <- fc4
I0821 15:14:39.915853 26133 net.cpp:380] fc5 -> fc5
I0821 15:14:39.915946 26133 net.cpp:129] Top shape: 128 1 (128)

I0821 15:14:39.916098 26133 net.cpp:406] loss <- fc5
I0821 15:14:39.916134 26133 net.cpp:406] loss <- labelp
I0821 15:14:39.916175 26133 net.cpp:380] loss -> loss
I0821 15:14:39.916220 26133 net.cpp:122] Setting up loss
I0821 15:14:39.916259 26133 net.cpp:129] Top shape: (1)
I0821 15:14:39.916292 26133 net.cpp:132]     with loss weight 1
'''
