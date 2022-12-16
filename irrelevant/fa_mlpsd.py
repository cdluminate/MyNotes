import os
import torch as th
import collections
from . import fashion, base
import yaml
from tqdm import tqdm
from .attacks import projectedGradientDescent
from termcolor import cprint, colored
from . import fa_mlp
from . import spre

class Model(fa_mlp.Model):
    def condition_regularization(self):
        c1 = spre.spre(self.fc1, True)
        c2 = spre.spre(self.fc2, True)
        c3 = spre.spre(self.fc3, True)
        return (c1+c2+c3)/3

    def loss(self, x, y, *, adv=True):  # note, adv is true
        device = self.fc1.weight.device
        images, labels = x.to(device), y.to(device).view(-1)
        if not adv:
            output = self.forward(images)
            loss = th.nn.functional.cross_entropy(output, labels)
            return output, loss
        else: # toggle adversarial training
            # baseline: forward original samples
            self.eval()
            with th.no_grad():
                output, loss = self.loss(images, labels, adv=False)
                acc_orig = (output.max(1)[1].eq(labels).sum().item()/len(y))
                loss_orig = loss.detach()
            # start PGD attack
            xr, r = projectedGradientDescent(self, images, labels,
                    eps=0.06, alpha=2./255., maxiter=12, verbose=False,
                    device=device, targeted=False, unbound=False)
            # forward the PGD adversary
            self.train()
            output, loss = self.loss(xr, labels, adv=False)
            acc_adv = (output.max(1)[1].eq(labels).sum().item()/len(y))
            loss_adv = loss.detach()
            # add CR
            loss_cr = self.condition_regularization()
            loss += loss_cr
            # mandatory report
            print('\t', colored('Orig loss', 'blue'),
                    '%.5f'%loss_orig, 'Acc', '%.3f'%acc_orig,
                    '|', colored('[Adv loss]', 'red'),
                    '%.5f'%loss.item(), 'Acc', '%.3f'%acc_adv,
                    '|', colored('CR', 'red'),
                    '%.5f'%loss_cr.item())
            return (output, loss)
