import sys
import os
import time
import argparse

from tqdm import tqdm
import numpy as np
import torch as th
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torchvision as vision


class Net(th.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = th.nn.Conv2d(1, 6, 5) # input channel, 6 out channel, 5x5 conv
        self.bn1 = th.nn.BatchNorm2d(6)
        self.conv2 = th.nn.Conv2d(6, 16, 5)
        self.bn2 = th.nn.BatchNorm2d(16)
        self.fc3 = th.nn.Linear(16*4*4, 120) # affine operation
        self.bn3 = th.nn.BatchNorm1d(120)
        self.fc4 = th.nn.Linear(120, 84)
        self.bn4 = th.nn.BatchNorm1d(84)
        self.fc5 = th.nn.Linear(84, 10)
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.bn1(self.conv1(x))), (2,2))
        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), 2)
        x = x.view(-1, np.prod(x.shape[1:]))
        x = F.relu(self.bn3(self.fc3(x)))
        x = F.relu(self.bn4(self.fc4(x)))
        x = self.fc5(x)
        return x


class DenseNet(th.nn.Module):
    '''
    https://arxiv.org/pdf/1608.06993.pdf
    densenet https://www.zhihu.com/question/60109389
    '''
    def __init__(self):
        super(DenseNet, self).__init__()
        self.b0l0 = th.nn.Sequential(
                th.nn.Conv2d(1, 8, kernel_size=5, stride=2, padding=2, bias=False),
                th.nn.BatchNorm2d(8),
                th.nn.ReLU(inplace=True),
                th.nn.MaxPool2d(kernel_size=2, stride=2, padding=1)
                )

        def _denselayer(in_channels, growth_rate):
            return th.nn.Sequential(
                    th.nn.BatchNorm2d(in_channels),
                    th.nn.ReLU(inplace=True),
                    th.nn.Conv2d(in_channels, 4*growth_rate, kernel_size=1, bias=False),
                    th.nn.BatchNorm2d(4*growth_rate),
                    th.nn.ReLU(inplace=True),
                    th.nn.Conv2d(4*growth_rate, growth_rate, kernel_size=3, stride=1, padding=1, bias=False)
                    )

        self.b1l0 = _denselayer(8, 8)
        self.b1l1 = _denselayer(16, 8)
        self.b1l2 = _denselayer(24, 8)
        self.b1tr = th.nn.Sequential(
                th.nn.BatchNorm2d(32),
                th.nn.ReLU(inplace=True),
                th.nn.Conv2d(32, 16, kernel_size=1, stride=1, bias=False),
                th.nn.AvgPool2d(kernel_size=2, stride=2, padding=0)
                )

        self.b2l0 = _denselayer(16, 8)
        self.b2l1 = _denselayer(24, 8)
        self.b2l2 = _denselayer(32, 8)
        self.b2tr = th.nn.Sequential(
                th.nn.BatchNorm2d(40),
                th.nn.ReLU(inplace=True),
                th.nn.Conv2d(40, 20, kernel_size=1, stride=1, bias=False),
                th.nn.AvgPool2d(kernel_size=2, stride=2)
                )

        self.b3nrm = th.nn.BatchNorm1d(80)
        self.b3aff = th.nn.Linear(80, 10)

    def forward(self, x):
        x = self.b0l0(x)

        b1l0 = self.b1l0(x)
        b1l1 = self.b1l1(th.cat([x, b1l0], dim=1))
        b1l2 = self.b1l2(th.cat([x, b1l0, b1l1], dim=1))
        b1tr = self.b1tr(th.cat([x, b1l0, b1l1, b1l2], dim=1))

        b2l0 = self.b2l0(b1tr)
        b2l1 = self.b2l1(th.cat([b1tr, b2l0], dim=1))
        b2l2 = self.b2l2(th.cat([b1tr, b2l0, b2l1], dim=1))
        b2tr = self.b2tr(th.cat([b1tr, b2l0, b2l1, b2l2], dim=1))

        b3nrm = self.b3nrm(b2tr.view(-1, 80))
        b3aff = self.b3aff(b3nrm)
        return b3aff


def assessment(model, dataloader, *, cuda) -> th.Tensor:
    '''
    Evaluate the given model on the given dataset.
    '''
    model.eval()
    with th.no_grad():
        preds, ground, losses = [], [], []
        for batchim, batchlb in tqdm(dataloader):
            batchim = batchim.cuda() if cuda else batchim
            batchlb = batchlb.cuda() if cuda else batchlb

            output = net(batchim)
            loss = crit(output, batchlb)

            pred = output.max(1)[1]  # argmax
            preds.append(pred.detach().cpu())
            ground.append(batchlb.detach().cpu())
            losses.append(loss.item())

        preds = th.cat(preds)
        ground = th.cat(ground)
        accuracy = preds.cpu().eq(ground.cpu()).sum().float() / preds.nelement()
        loss = th.sum(th.tensor(losses))
    return loss, accuracy



if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.add_argument('--cuda', action='store_true')
    ag.add_argument('--pool', type=str, default=os.path.expanduser('~/data'))
    ag.add_argument('--maxepoch', type=int, default=9)
    ag.add_argument('--display', type=int, default=20)
    ag.add_argument('--lr', type=float, default=1e-3)
    ag = ag.parse_args()

    #net = Net() if not ag.cuda else Net().cuda()
    net = DenseNet() if not ag.cuda else DenseNet().cuda()
    print(net)

    crit = th.nn.CrossEntropyLoss()
    print(crit)

    optim = th.optim.Adam(net.parameters(), lr=ag.lr, weight_decay=1e-5)
    print(optim)

    transform = vision.transforms.ToTensor()
    mnist = vision.datasets.MNIST(ag.pool, transform=transform)
    mnist_test = vision.datasets.MNIST(ag.pool, transform=transform, train=False)
    dataloader = DataLoader(mnist, batch_size=128, shuffle=True, pin_memory=True)
    dataloader_test = DataLoader(mnist_test, batch_size=128, shuffle=False, pin_memory=True)
    print(mnist)
    print(mnist_test)

    for eph in range(ag.maxepoch):

        loss, accu = assessment(net, dataloader_test, cuda=ag.cuda)
        print(f'Eph[{eph}]',
                f'Loss {loss.item():.4f}',
                f'Accu {accu.item():.4f}',
                sep='\t')

        if (eph+1)%3 == 0:
            for param_group in optim.param_groups:
                param_group['lr'] *= 0.1

        for lit, (batchim, batchlb) in enumerate(dataloader):
            git = lit + eph * len(dataloader)
            batchim = batchim.cuda() if ag.cuda else batchim
            batchlb = batchlb.cuda() if ag.cuda else batchlb

            net.train()
            output = net(batchim)
            loss = crit(output, batchlb)
            optim.zero_grad()
            loss.backward()
            optim.step()

            with th.no_grad():
                pred = output.max(1)[1]  # argmax
                accuracy = pred.cpu().eq(batchlb.cpu()).sum().float() / pred.nelement()

            if git % ag.display == 0:
                print(f'Eph[{eph}][{lit}/{len(dataloader)}]',
                        f'Loss {loss.item():.3f}',
                        f'Accu {accuracy.item():.3f}',
                        sep='\t')

'''
$ optirun python3 th_convnet.py --cuda
'''
