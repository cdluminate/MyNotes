'''
Spatial Transformer Networks
  -- generalization of differentiable attention to spatial transformation
  -- geometric invariance by learning spatial transformations

:ref: https://pytorch.org/tutorials/intermediate/spatial_transformer_tutorial.html
:ref: https://arxiv.org/abs/1506.02025
'''
import os, sys, re
import argparse
import torch as th
import numpy as np
import torchvision as vision
import tensorboardX as TBX


class STN(th.nn.Module):
    def __init__(self):
        super(STN, self).__init__()

        # Basic Conv Net
        self.cnn = th.nn.Sequential(
                th.nn.Conv2d(1, 10, kernel_size=5),
                th.nn.MaxPool2d(2),
                th.nn.ReLU(True),
                th.nn.Conv2d(10, 20, kernel_size=5),
                th.nn.Dropout2d(),
                th.nn.MaxPool2d(2),
                th.nn.ReLU(True)
                )
        self.fc = th.nn.Sequential(
                th.nn.Linear(320, 50),
                th.nn.ReLU(True),
                th.nn.Dropout(),
                th.nn.Linear(50, 10)
                )

        # Spatial Transformer localization network
        self.localization = th.nn.Sequential(
                th.nn.Conv2d(1, 8, kernel_size=7),
                th.nn.MaxPool2d(2, stride=2),
                th.nn.ReLU(True),  # inplace relu
                th.nn.Conv2d(8, 10, kernel_size=5),
                th.nn.MaxPool2d(2, stride=2),
                th.nn.ReLU(True)
                )
        # Regressor for the 3*2 affine matrix
        self.loc_fc = th.nn.Sequential(
                th.nn.Linear(10*3*3, 32),
                th.nn.ReLU(True),
                th.nn.Linear(32, 3*2)
                )

        # identity transformation
        self.loc_fc[2].weight.data.zero_()
        self.loc_fc[2].bias.data.copy_(
                th.tensor([1, 0, 0, 0, 1, 0], dtype=th.float))

    def forwardSTN(self, x):
        xs = self.localization(x).view(-1, 10*3*3)
        theta = self.loc_fc(xs).view(-1, 2, 3)
        grid = th.nn.functional.affine_grid(theta, x.size())
        x = th.nn.functional.grid_sample(x, grid)
        return x

    def forward(self, x):
        x = self.forwardSTN(x)
        x = self.cnn(x).view(-1, 320)
        x = self.fc(x)
        x = th.nn.functional.log_softmax(x, dim=1)
        return x


def getLoaderMNIST(root: str):
    transform = vision.transforms.Compose([
        vision.transforms.ToTensor(),
        vision.transforms.Normalize((0.1307,), (0.3081,)) ])
    trainset = vision.datasets.MNIST(root=root, train=True, download=True,
            transform=transform)
    testset  = vision.datasets.MNIST(root=root, train=False,
            transform=transform)
    trainloader = th.utils.data.DataLoader(trainset,
            batch_size=64, shuffle=True, pin_memory=True)
    testloader = th.utils.data.DataLoader(testset,
            batch_size=64, shuffle=False, pin_memory=False)
    return trainloader, testloader


def evaluate(model, loader, tbx, git, *, ag):
    with th.no_grad():
        model.eval()
        allpred, alllabel = th.tensor([], dtype=th.long), th.tensor([], dtype=th.long)
        if ag.cuda:
            allpred, alllabel = allpred.cuda(), alllabel.cuda()
        for data, label in loader:
            if ag.cuda:
                data, label = data.cuda(), label.cuda()
            output = model(data)
            pred = output.max(1)[1]
            allpred = th.cat((allpred, pred), dim=0)
            alllabel = th.cat((alllabel, label), dim=0)
        accu = alllabel.eq(allpred).sum().item() / alllabel.nelement()
        print('Test', 'accu', accu)

    tbx.add_scalar('test/accuracy', accu, git)


def tensor2numpy(x):
    x = x.detach().cpu().numpy().transpose((1,2,0))
    mean = np.array([0.485, 0.456, 0.406])
    std  = np.array([0.229, 0.224, 0.225])
    x    = std * x + mean
    x    = np.clip(x, 0., 1.)
    return x


def train_(model, crit, optim, data, ag, *, report=False, tbx, git):
    '''
    perform one forward-backward-update loop
    '''
    output = model(data)
    loss = crit(output, label)
    optim.zero_grad()
    loss.backward()
    optim.step()

    if report:
        pred = output.max(1)[1]
        accu = label.eq(pred).sum().item() / pred.nelement()
        print(f'Eph[{eph}][{iteration}/{len(trainloader)}]',
                f'loss', loss.item(),
                f'accu', accu)

        tbx.add_scalar('train/loss', loss.item(), git)

        with th.no_grad():
            orig   = data.cpu()
            stnout = model.forwardSTN(data).cpu()

            orig_grid = vision.utils.make_grid(orig)
            stnout_grid = vision.utils.make_grid(stnout)

            tbx.add_image('image/orig', tensor2numpy(orig_grid), git)
            tbx.add_image('image/stn', tensor2numpy(stnout_grid), git)


if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.add_argument('--cuda', default=False, action='store_true')
    ag.add_argument('--pool', type=str, default='..')
    ag = ag.parse_args()

    tbx = TBX.SummaryWriter('runs/XXX')

    print('> load data')
    trainloader, testloader = getLoaderMNIST(ag.pool)

    print('> create model')
    model = STN()
    model = model.cuda() if ag.cuda else model
    print(model)

    print('> crit and optim')
    crit = th.nn.functional.nll_loss
    optim = th.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)

    for eph in range(20):
        evaluate(model, testloader, tbx, eph*len(trainloader), ag=ag)

        for iteration, (data, label) in enumerate(trainloader):

            git = eph * len(trainloader) + iteration
            if ag.cuda:
                data, label = data.cuda(), label.cuda()

            train_(model, crit, optim, data, ag,
                    report = True if (git % 64 == 0) else False,
                    tbx=tbx, git=git)

    evaluate(model, testloader, tbx, eph*len(trainloader), ag=ag)
