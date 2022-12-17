'''
https://github.com/pytorch/examples/blob/master/mnist/main.py
'''
import os
import sys
import argparse

import numpy as np
import torch as th
import torch.nn.functional as functional
import torchvision as vision
from tqdm import tqdm


class Model(th.nn.Module):
    '''
    Convnet module
    '''
    def __init__(self):
        super(Model, self).__init__()
        self.conv1 = th.nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = th.nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = th.nn.Dropout2d()
        self.fc1 = th.nn.Linear(320, 50)
        self.fc2 = th.nn.Linear(50, 10)

    def forward(self, x):
        x = functional.relu(functional.max_pool2d(self.conv1(x), 2))
        x = functional.relu(functional.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = functional.relu(self.fc1(x))
        x = functional.dropout(x, training=self.training)
        x = self.fc2(x)
        return functional.log_softmax(x, dim=1)


def dlTrain(ag, model, dataloader, optim, epoch):
    model.train()
    for iteration, (images, labels) in enumerate(dataloader):
        images = images.to(ag.device)
        labels = labels.to(ag.device)
        optim.zero_grad()

        output = model(images)
        loss = functional.nll_loss(output, labels)
        loss.backward()
        optim.step()

        pred = output.max(1)[1]
        acc1 = 100.*pred.eq(labels).sum().item() / len(labels)

        if iteration % ag.reportevery == 0:
            print(f'Eph[{epoch}][{iteration}/{len(dataloader)}]',
                    f'\tloss {loss.item():.3f}', f'\tAcc@1 {acc1:.1f}%')


def dlValidate(ag, model, dataloader, epoch):
    model.eval()
    test_loss, correct = 0, 0
    with th.no_grad():
        for iteration, (images, labels) in tqdm(enumerate(dataloader), total=len(dataloader)):
            images = images.to(ag.device)
            labels = labels.to(ag.device)

            output = model(images)
            loss = functional.nll_loss(output, labels, reduction='sum')
            test_loss += loss.item()
            pred = output.max(1, keepdim=True)[1].view(-1)
            correct += pred.eq(labels).sum().item()

    test_loss /= len(dataloader)
    print(f'Validation@Eph[{epoch}]', f'\tloss {test_loss:.4f}',
            f'\tAcc@1 {100.*correct/len(dataloader.dataset):.2f}')


def mainTrain(argv):
    ag = argparse.ArgumentParser()
    ag.add_argument('--batch', type=int, default=64)
    ag.add_argument('--epochs', type=int, default=10)
    ag.add_argument('--lr', type=float, default=1e-2)
    ag.add_argument('-D', '--device', type=str, default='cpu')
    ag.add_argument('--reportevery', type=int, default=50)
    ag = ag.parse_args(argv)
    ag.device = th.device(ag.device)

    # load datasets
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

    # create model and optimizer
    model = Model().to(ag.device)
    optim = th.optim.SGD(model.parameters(), lr=ag.lr, momentum=0.9)

    # start training
    dlValidate(ag, model, test_loader, -1)
    for epoch in range(ag.epochs):
        dlTrain(ag, model, train_loader, optim, epoch)
        dlValidate(ag, model, test_loader, epoch)


if __name__ == '__main__':
    eval(f'main{sys.argv[1]}')(sys.argv[2:])
