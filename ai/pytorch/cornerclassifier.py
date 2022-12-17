#!/usr/bin/python3
'''
Simple Corner Classifier
'''
import os, sys, re
import torch as th
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.dataset import Subset
from torchvision import transforms
import cv2
import numpy as np
import glob
from PIL import Image
import random
import argparse


class CornerDataset(Dataset):
    def __init__(self, repool: str = 'DATA/train/*.JPEG'):
        jpgs = glob.glob(repool, recursive=True)
        print(f'* found {len(jpgs)} images.')
        self.samples = []
        print(f'> processing dataset ...')
        for jpg in jpgs:
            image = Image.open(jpg).convert('RGB')
            image = transforms.Resize(64)(image)
            image = transforms.ToTensor()(image)
            cor_tl = image[:, 0:25, 0:25]
            self.samples.append((cor_tl, 0))
            cor_tr = image[:, 39:64, 0:25]
            self.samples.append((cor_tr, 1))
            cor_bl = image[:, 0:25, 39:64]
            self.samples.append((cor_bl, 3))
            cor_br = image[:, 39:64, 39:64]
            self.samples.append((cor_br, 2))
        print(f'> dataset size {len(self.samples)}')
        random.shuffle(self.samples)
        print(f'> stat', self.samples[0][0].max())
    def __len__(self):
        return len(self.samples)
    def __getitem__(self, index):
        return self.samples[index]
    def getCollate(self):
        def _collate(data):
            image, label = zip(*data)
            image = th.stack(image)
            return image, th.LongTensor(label)
        return _collate


class Model(th.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.conv1 = th.nn.Conv2d(3, 32, 5, stride=1, padding=0)
        self.bn1   = th.nn.BatchNorm2d(32)
        self.pool1 = th.nn.MaxPool2d(3, stride=2, padding=1)
        self.conv2 = th.nn.Conv2d(32, 64, 5, stride=1, padding=0)
        self.bn2   = th.nn.BatchNorm2d(64)
        self.pool2 = th.nn.MaxPool2d(3, stride=2, padding=1)
        self.fc3   = th.nn.Linear(1024, 128)
        self.bn3   = th.nn.BatchNorm1d(128)
        self.fc4   = th.nn.Linear(128, 4)
    def forward(self, images):
        x = self.conv1(images)
        x = self.bn1(x)
        x = th.nn.functional.relu(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = th.nn.functional.relu(x)
        x = self.pool2(x)
        x = x.view(images.shape[0], -1)
        x = self.fc3(x)
        x = self.bn3(x)
        x = th.nn.functional.relu(x)
        x = self.fc4(x)
        return x


def evaluate(model, valloader, ifsave = False, *, best=[0.], cuda=False):
    model.eval()
    for image, label in valloader:
        image = image.cuda() if cuda else image
        label = label.cuda() if cuda else label
        out = model(image)
        pred = out.max(1)[1]
        correct = pred.eq(label).sum()
        accu = 100*correct/image.shape[0]
        if ifsave and accu > best[0]:
            best[0] = accu
            th.save([model.state_dict(), accu], 'model.best.pth')
        break
    print(f'TEST: accu: {accu}, bset: {best[0]}')


def predict(model, images, writeto):
    model.eval()
    model.cpu()
    writeto = open(writeto, 'w')
    for jpg in images:
        image = Image.open(jpg).convert('RGB')
        image = transforms.Resize(25)(image)
        image = transforms.ToTensor()(image)
        image = image.unsqueeze(0)
        out = model(image)
        pred = out.max(1)[1]
        basename = os.path.basename(jpg)
        print(basename, pred.item())
        writeto.write(f'{basename},{pred.item()}\n')
    writeto.close()


if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.add_argument('--cuda', action='store_true', default=False)
    ag.add_argument('--snap', type=str, default=False)
    ag.add_argument('--pred', type=str, default=False)
    ag.add_argument('--result', type=str, default=False)
    ag = ag.parse_args()

    dataset = CornerDataset()
    valset = Subset(dataset, range(1000))
    trainset = Subset(dataset, range(1000, len(dataset)))
    loader = DataLoader(trainset, batch_size=128, shuffle=True,
            pin_memory=True, collate_fn=dataset.getCollate())
    valloader = DataLoader(valset, batch_size=1000, shuffle=False,
            collate_fn=dataset.getCollate())

    model = Model()
    if ag.snap:
        state_dict, accu = th.load(ag.snap)
        print('> Loading pretrained model', ag.snap, 'accuracy', accu)
        model.load_state_dict(state_dict)
    model = model.cuda() if ag.cuda else model
    crit = th.nn.CrossEntropyLoss()
    optim = th.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)

    if ag.pred:
        assert(ag.snap)
        testfiles = glob.glob(ag.pred+'/**.JPEG')
        if ag.result:
            predict(model, testfiles, ag.result)
        else:
            predict(model, testfiles, 'test_results.txt')
        exit()

    for eph in range(50):
        if ag.snap: break

        evaluate(model, valloader, True if not ag.snap else False,
                cuda=ag.cuda)

        for iter, (image, label) in enumerate(loader):
            giter = eph * len(loader) + iter
            model.train()

            image = image.cuda() if ag.cuda else image
            label = label.cuda() if ag.cuda else label
            out = model(image)
            loss = crit(out, label)

            optim.zero_grad()
            loss.backward()
            optim.step()

            pred = out.max(1)[1]
            correct = pred.eq(label).cpu().sum()
            accu = 100*correct/image.shape[0]

            print(f'* Eph[{eph}][{iter}/{len(loader)}]:',
                    f'loss {loss.item():.3f}',
                    f'accu {accu:4.1f}')

        if eph == 30:
            optim = th.optim.Adam(model.parameters(), lr=1e-5, weight_decay=1e-5)

    evaluate(model, valloader, True if not ag.snap else False,
            cuda=ag.cuda)

'''
Accuracy 88% on validation set.
>>> optirun python3 cornerclassifier.py --cuda
>>> optirun python3 cornerclassifier.py --cuda --snap model.best.pth
>>> optirun python3 cornerclassifier.py --cuda --snap model.best.pth --pred DATA/test_crop_easy --result test_crop_easy.txt
>>> optirun python3 cornerclassifier.py --cuda --snap model.best.pth --pred DATA/test_crop_hard --result test_crop_hard.txt
'''
