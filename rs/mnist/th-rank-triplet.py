# Reference: https://github.com/andreasveit/triplet-network-pytorch
import sys
import os
import argparse
import json
from collections import OrderedDict
import random
import time
import numpy as np
import codecs
import csv
from PIL import Image

raise SystemExit("WIP")

## One-line timer function
def tic(): return eval("lambda: time.time() - {}".format(time.time()))

## Load Pytorch
import torch as th
from torch.autograd import Variable
import torch.nn.functional as F
print("using Torch", th.__version__)

## Argument
argp = argparse.ArgumentParser(description='PyTorch Embedding')
argp.add_argument('-g', '--gpu', action='store_true', help='use CUDA')
argp.add_argument('-m', '--maxiter', type=int, default=5000, help='max iter')
argp.add_argument('-j', '--jobs', type=int, default=4, help='*_NUM_THREADS')
argp.add_argument('-t', '--tp', type=int, default=100, help='test period')
argp.add_argument('-l', '--lr', type=float, default=1e-3, help='learning rate')
argp.add_argument('-b', '--batch', type=int, default=256, help='batchsize')
argp.add_argument('--margin', type=float, default=0.2, help='margin')
argp.add_argument('--code', type=str, default='', help='experiment codename')
argp.add_argument('--weight', type=str, help='load weight from model')
args = argp.parse_args()
print("-> Dump arguments")
print(json.dumps(vars(args), indent=2))

## BLAS, Torch, CUDA setup
os.putenv('OPENBLAS_NUM_THREADS', str(args.jobs))
os.putenv('OMP_NUM_THREADS', str(args.jobs))
os.putenv('MKL_NUM_THREADS', str(args.jobs))
th.manual_seed(666)
if args.gpu: th.cuda.manual_seed(666)
TENSOR_T = 'torch.cuda.FloatTensor' if args.gpu else 'torch.FloatTensor'
th.set_default_tensor_type(TENSOR_T)
th.backends.cudnn.benchmark = True # enable cuDNN auto-tuner

## Model setup
class TripletNet(nn.Module):
    def __init__(self, embnet):
        super(TripletNet, self).__init__()
        self.embnet = embnet
    def forward(self, x, y, z):
        emb_x = self.embnet(x)
        emb_y = self.embnet(y)
        emb_z = self.embnet(z)
        dist_xy = F.pairwise_distance(emb_x, emb_y, 2)
        dist_xz = F.pairwise_distance(emb_x, emb_z, 2)
        return dist_xy, dist_xz, emb_x, emb_y, emb_z

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = th.nn.Conv2D(1, 10, kernel_size=5)
        self.conv2 = th.nn.Conv2D(10, 20, kernel_size=5)
        self.conv2_drop = th.nn.Dropout2D()
        self.fc1 = th.nn.Linear(320, 50)
        self.fc2 = th.nn.Linear(50, 10)
    def forward(self, x):
        x = F.relu(F.max_pool2d(self,conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, traning=self.training)
        return self.fc2(x)

Model_net = Net()
Model = TripletNet(Model_net)
model = Model().float().cuda() if args.gpu else Model().float()
if args.resume: # FIXME
    checkpoint = torch.load(args.resume)
    model.load_state_dict(checkpoint['state_dict'])
print(model)
print('-> Number of learnable parameters: {}'.format(
    sum([p.data.nelement() for p in model.parameters()]) ))

## Loss and Optimizer
crit = th.nn.MarginRankingLoss(margin = args.margin)
optimizer = th.optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-5)

## Data Loader
class mnistLoader(th.utils.data.Dataset):
    urls = [
            'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
            ]

    @staticmethod
    def getInt(b):
        return int(codecs.encode(b, 'hex'), 16)

    @staticmethod
    def parseByte(b):
        return ord(b) if isinstance(b, str) else b

    @staticmethod
    def readLabelFile(fpath):
        with open(fpath, 'rb') as f:
            data = f.read()
            assert(getInt(data[:4]) == 2049)
            length = getInt(data[4:8])
            labels = [parseByte(b) for b in data[8:]]
            assert(len(labels) == length)
            return torch.LongTensor(labels)

    @staticmethod
    def readImageFile(fpath):
        with open(fpath, 'rb') as f:
            data = f.read()
            assert(getInt(data[:4]) == 2051)
            length = getInt(data[4:8])
            num_rows = getInt(data[8:12])
            num_cols = getInt(data[12:16])
            images = []
            idx = 16
            for l in range(length):
                img = []
                images.append(img)
                for r in range(num_rows):
                    row = []
                    img.append(row)
                    for c in range(num_cols):
                        row.append(parseByte(data[idx]))
                        idx += 1
            assert(len(images) == length)
            return torch.ByteTensor(images).view(-1, 28, 28)

    @staticmethod
    def makeTripletList(self, ntriplets):
        if self.train:
            np_labels = self.train_labels.numpy()
            fname = self.train_triplet_file
        else:
            np_labels = self.test_labels.numpy()
            fname = self.test_triplet_file
        triplets = []
        for class_idx in range(10):
            a = np.random.choice(np.where(np_labels==class_idx)[0],
                    int(ntriplets/10), replace=True)
            b = np.random.choice(np.where(np_labels==class_idx)[0],
                    int(ntriplets/10), replace=True)
            while (np.any((a-b)==0)):
                np.random.shuffle(b)
            c = np.random.choice(np.where(np_labels!=class_idx)[0],
                    int(ntriplets/10), replace=True)
            for i in range(a.shape[0]):
                triplets.append([int(a[i]), int(c[i]), int(b[i])])
        with open(fname, 'wb') as f:
            writer = csv.writer(f, delimiter=' ')
            writer.writerows(triplets)
    def __len__(self):
        if self.train:
            return len(self.triplets_train)
        else:
            return len(self.triplets_test)
    def __getitem__(self, idx):
        if self.train:
            i1, i2, i3 = self.triplets_train[idx]
            p1, p2, p3 = self.train_data[i1], self.train_data[i2], \
                    self.train_data[i3]
        else:
            i1, i2, i3 = self.triplets_test[idx]
            p1, p2, p3 = self.test_data[i1], self.test_data[i2], \
                    self.test_data[i3]
        p1 = Image.fromarray(p1.numpy(), mode='L')
        p2 = Image.fromarray(p2.numpy(), mode='L')
        p3 = Image.fromarray(p3.numpy(), mode='L')
        return p1, p2, p3
    def __init__(self, n_train_triplets, n_test_triplets, train=True,
            transform=None, target_transform=None):
        self.root = root
        self.transform = transform
        self.train = train
        if self.train:
            self.train_data, self.train_labels = torch.load
# FIXME
#kwargs = {'num_workers': 1, 'pin_memory': True} if args.cuda else {}
#train_loader = torch.utils.data.DataLoader(
#    MNIST_t('../data', train=True, download=True,
#                   transform=transforms.Compose([
#                       transforms.ToTensor(),
#                       transforms.Normalize((0.1307,), (0.3081,))
#                   ])),
#    batch_size=args.batch_size, shuffle=True, **kwargs)
#test_loader = torch.utils.data.DataLoader(
#    MNIST_t('../data', train=False, transform=transforms.Compose([
#                       transforms.ToTensor(),
#                       transforms.Normalize((0.1307,), (0.3081,))
#                   ])),
#    batch_size=args.batch_size, shuffle=True, **kwargs)

## Preprocess function
def prepro_v1(xbatch, ybatch):
  xbatch = xbatch / 255
  xbatch = Variable(th.from_numpy(xbatch), requires_grad=False).float()
  ybatch = Variable(th.from_numpy(ybatch), requires_grad=False).long()
  if args.gpu: xbatch, ybatch = xbatch.cuda(), ybatch.cuda()
  return xbatch, ybatch
prepro_v2 = prepro_v1
prepro = eval("prepro_{}".format(Model.__name__.split('_')[-1])) # symlink

## Data Fetching function
def getBatch(train:bool, trainrange=[], testrange=[]):
  # load batch and pre-process
  if train:
      if not trainrange:
        idx = list(range(X_train.shape[0]))
        random.shuffle(idx)
        idx = idx[:args.batch]
      else:
        idx = trainrange
  else:
    idx = testrange
  x_batch = (X_train if train else X_test)[idx, :]
  y_batch = (y_train if train else y_test)[idx]
  x_batch, y_batch = prepro(x_batch, y_batch)
  return x_batch, y_batch

## Train and Evaluation function
def train(loader, model, crit, optim, iteration):

def evaluation(i: int):
  # forward
  model.eval()
  losses = []
  accuracies = []
  for j in range(int(y_test.shape[0]/args.batch)):
    x_batch, y_batch = getBatch(train=False,
        testrange=list(range(j*args.batch, (j+1)*args.batch)))
    modelout = model(x_batch)
    loss = crit(modelout, y_batch)
    # statistics
    pred = modelout.data.max(1)[1]
    correct = pred.eq(y_batch.data).sum()
    accuracy = correct / modelout.size(0)
    losses.append(loss.data[0])
    accuracies.append(accuracy)
  loss = sum(losses)/len(losses)
  accuracy = sum(accuracies)/len(accuracies)
  print('Test @', end=' ')
  print('iter {:>5d}'.format(i), end='\t|\t')
  print('loss {:>10.3f}'.format(loss), end='\t|\t')
  print('accu {:>9.4f}'.format(accuracy), end='\t|\t')
  print()
  return loss, accuracy

## Recording
test_loss = []
train_loss = []

## Main loop
for i in range(args.maxiter+1):
    l = train(train_loader, model, crit, optimizer, i)
    train_loss.append(l)
    # periodical model test and save
    if i % args.tp == 0:
        l = evaluation(test_loader, model, crit, optimizer, i)
        test_loss.append(l)
        snapshot(model, code, i)

  # load data
  toc = tic()
  trainrange = list(map( lambda x: x%y_train.shape[0],
                 list(range(i*args.batch, (i+1)*args.batch))
               ))
  x_batch, y_batch = getBatch(train=True, trainrange=trainrange)
  #x_batch, y_batch = getBatch(train=True) # random sampling
  loadtoc = toc()

  # decay learning rate
  if i > 1000:
    lr = args.lr * (0.5 ** ((i-1000)/2000))
    for param_group in optimizer.param_groups:
      param_group['lr'] = lr
  # forward, backward, update
  toc = tic()
  model.train()
  modelout = model(x_batch)
  loss = crit(modelout, y_batch)
  optimizer.zero_grad()
  loss.backward()
  optimizer.step()
  toc = toc()
  # report
  pred = modelout.data.max(1)[1]
  correct = pred.eq(y_batch.data).sum()
  accuracy = correct / modelout.size(0)
  print('Training @', end=' ')
  print('iter {:>5d}'.format(i), end='\t|\t')
  print('loss {:>10.3f}'.format(loss.data[0]), end='\t|\t')
  print('accu {:>9.4f}'.format(accuracy), end='\t|\t')
  print('time/ms {:5.3f}'.format(toc*1e3), end='\t|\t')
  print('loadtime/ms {:5.3f}'.format(loadtoc*1e3), end='\t|\t')
  print()

## Final Data Dump
print('test_loss', test_loss)
print('test_accu', test_accu)
