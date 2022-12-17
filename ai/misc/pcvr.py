'''
Pretrained Contextual Visual Representation
'''
import sys, os, json, argparse
import numpy as np
import torch as th
import torchvision as vision
import blessings
import tqdm
from collections import namedtuple


Snapshot = namedtuple('Snapshot', ['arguments', 'iteration', 'state_dict', 'loss', 'comments'])


class PCVR(th.nn.Module):
    '''
    The PCVR Model
    '''
    def __init__(self, in_features, hid_features, *, rnntype='LSTM'):
        super(PCVR, self).__init__()
        for attr in ('in_features', 'hid_features', 'rnntype'):
            setattr(self, attr, eval(attr))
        #self.rnnlr = th.nn.LSTM(in_features, hid_features)
        #self.rnnrl = th.nn.LSTM(in_features, hid_features)
        self.rnntb = th.nn.LSTM(in_features, hid_features, batch_first=True)  # top->bottom
        #self.rnnbt = th.nn.LSTM(in_features, hid_features)
    def forward(self, x):
        '''
        input shape: (batch_size, channel, height, width)
        '''
        x_tb = x.transpose(1,2).contiguous().view(x.size(0), x.size(2), -1)
        output, (hn, cn) = self.rnntb(x_tb)
        return output


class MnistModel(th.nn.Module):
    '''
    PCVR on Mnist
    '''
    def __init__(self, hid_features):
        super(MnistModel, self).__init__()
        self.pcvr = PCVR(28, 28*hid_features)
        self.linear = th.nn.Linear(28*hid_features, 28)
    def forward(self, x):
        r = self.pcvr(x)
        pred = th.sigmoid( self.linear( th.nn.functional.relu( r)))
        return pred


def _loadDataset(ag):
    train_loader = th.utils.data.DataLoader(
            vision.datasets.MNIST(f'{os.getenv("HOME")}/.torch/mnist/', train=True, download=True,
                transform=vision.transforms.Compose([
                    vision.transforms.ToTensor(),
                    vision.transforms.Normalize((0.1307,), (0.3081,))
                    ])),
                batch_size=ag.batch, shuffle=True, num_workers=1, pin_memory=True)
    test_loader = th.utils.data.DataLoader(
            vision.datasets.MNIST(f'{os.getenv("HOME")}/.torch/mnist/', train=False,
                transform=vision.transforms.Compose([
                    vision.transforms.ToTensor(),
                    vision.transforms.Normalize((0.1307,), (0.3081,))
                ])),
                batch_size=ag.batch, shuffle=False, num_workers=1, pin_memory=True)
    return train_loader, test_loader


def Train(argv):
    '''
    Train the model
    '''
    ag = argparse.ArgumentParser()
    ag.add_argument('-D', '--device', type=str, default='cpu')
    ag.add_argument('--batch', type=int, default=128)
    ag.add_argument('--maxepoch', type=int, default=15)
    ag = ag.parse_args(argv)
    ag.device = th.device(ag.device)
    T = blessings.Terminal()
    print(T.on_color(162)('>> Dump Arguments ...'))
    for (k, v) in vars(ag).items():
        print(f'   | {T.red}{k}{T.normal}\t {v}')

    # load dataset
    print(T.on_color(162)('>> Loading Dataset ...'))
    train_loader, test_loader = _loadDataset(ag)
    print(train_loader.dataset)
    print(test_loader.dataset)

    # create model
    print(T.on_color(162)('>> Creating Model ...'))
    model = MnistModel(4).to(ag.device)

    # create optimizer
    print(T.on_color(162)('>> Creating Optimizer ...'))
    optim = th.optim.Adam(model.parameters(), lr=1e-3)

    # start training
    print(T.on_color(162)('>> Starting Traning ...'))
    for epoch in range(ag.maxepoch):
        print(T.on_color(92)(f'> Training @ Eph {epoch}'))
        for iteration, (images, labels) in enumerate(train_loader):
            images = images.to(ag.device)

            optim.zero_grad()
            pred = model(images)
            loss = th.nn.functional.mse_loss(pred, images)
            loss.backward()
            optim.step()

            print(T.color(42)(f'Eph[{epoch}][{iteration}/{len(train_loader)}]'),
                    loss.item())
        print('Saving checkpoint ...')
        snapshot = Snapshot(arguments=ag, iteration=epoch*len(train_loader),
                state_dict=model.state_dict(), loss=loss.item(), comments=None)
        th.save(tuple(snapshot), 'snapshot_latest.pth')


if __name__ == '__main__':
    eval(f'{sys.argv[1]}')(sys.argv[2:]) if sys.argv[1:] else exit(1)
