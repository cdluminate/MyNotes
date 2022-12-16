import os
import torch as th
import collections
from . import cifar100
import yaml
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
from . import ct_res18


class Model(ct_res18.Model):
    def __init__(self):
        super(Model, self).__init__()
        self.net = ct_res18.ResNet18()
        self.net.linear = nn.Linear(512, 100, bias=True)  # tiny surgery
    def forward(self, x):
        return self.net(x)

    def getloader(self, kind:str='train', batchsize:int=1):
        '''
        get corresponding dataloaders
        '''
        config = yaml.load(open('config.yml', 'r').read(), Loader=yaml.SafeLoader)
        if kind == 'train':
            return cifar100.get_loader(os.path.expanduser(config['cifar100']['path']), batchsize, 'train')
        else:
            return cifar100.get_loader(os.path.expanduser(config['cifar100']['path']), batchsize, 'test')
