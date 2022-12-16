import os
import torch as th
import collections
from . import fashion, common, abstract
from . import classify
import yaml
from tqdm import tqdm


class Model(abstract.Model):
    """
    Softmax + cross entropy
    """
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = th.nn.Linear(28*28, 10)

    def forward(self, x):
        # -1, 1, 28, 28
        x = x.view(-1, 28*28)
        # -1, 28*28
        x = self.fc1(x)
        return x

    def getloader(self, kind:str='train', batchsize:int=1):
        '''
        get corresponding dataloaders
        '''
        config = yaml.load(open('config.yml', 'r').read(),
                Loader=yaml.SafeLoader)
        if kind == 'train':
            return fashion.get_loader(
                    os.path.expanduser(config['fashion-mnist']['path']),
                    batchsize, 'train')
        else:
            return fashion.get_loader(
                    os.path.expanduser(config['fashion-mnist']['path']),
                    batchsize, 't10k')

    def loss(self, x, y, *, adv=False):
        device = self.fc1.weight.device
        images, labels = x.to(device), y.to(device).view(-1)
        output = self.forward(images)
        loss = th.nn.functional.cross_entropy(output, labels)
        return output, loss

    def report(self, epoch, iteration, total, output, labels, loss):
        result = classify.cls_report(output, labels, loss)
        print(f'Eph[{epoch}][{iteration}/{total}]', result)

    def validate(self, dataloader):
        device = self.fc1.weight.device
        return classify.cls_validate(self, dataloader)

    def attack(self, att, loader, *, dconf, verbose=False):
        device = self.fc1.weight.device
        return classify.cls_attack(self, att, loader,
                dconf=dconf, device=device, verbose=verbose)
