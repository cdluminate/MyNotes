import os
import torch as th
import collections
from . import fashion, base
import yaml
from tqdm import tqdm
from .attacks import projectedGradientDescent
from termcolor import cprint, colored
from . import fa_c2f2
from . import spre

class Model(fa_c2f2.Model):
    def condition_regularization(self):
        # XXX: self.modules ...
        # self.conv1 = th.nn.Conv2d(1, 32, kernel_size=5, padding=2)
        # self.conv2 = th.nn.Conv2d(32, 64, kernel_size=5, padding=2)
        # self.fc1 = th.nn.Linear(64*7*7, 1024)
        # self.fc2 = th.nn.Linear(1024, 10)
        c1 = spre.spre(self.fc1, True)
        c2 = spre.spre(self.fc2, True)
        return (c1+c2)/2

    def loss(self, x, y, *, adv=True):  # note, adv is true
        device = self.fc1.weight.device
        images, labels = x.to(device), y.to(device).view(-1)
        if not adv:
            output = self.forward(images)
            loss = th.nn.functional.cross_entropy(output, labels)
            return output, loss
        else: # toggle adversarial training
            # baseline: forward original samples
            output, loss_ce = self.loss(images, labels, adv=False)
            acc_orig = (output.max(1)[1].eq(labels).sum().item()/len(y))
            # CR
            loss_cr = self.condition_regularization()
            # sum
            loss = loss_ce + 1.0 * loss_cr
            # mandatory report
            print('\t', colored('CE', 'blue'),
                    '%.5f'%loss_ce.item(), 'Acc', '%.3f'%acc_orig,
                    '|', colored('CR', 'red'),
                    '%.5f'%loss_cr.item())
            return (output, loss)
