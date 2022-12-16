import os
import torch as th
import collections
from . import fashion, base
import yaml
from tqdm import tqdm
from .attacks import projectedGradientDescent
from termcolor import cprint, colored
from . import fa_softmax

'''
Condition Regularization
'''

def condition(mod: th.nn.Module):
    if isinstance(mod, th.nn.Linear):
        A, Ap = mod.weight, th.pinverse(mod.weight)
        σ = th.svd(A).S.max()
        σp = th.svd(Ap).S.max()
        core = th.log(σ * σp).relu()
    else:
        raise TypeError(mod)
    return core


class Model(fa_softmax.Model):
    def condition_regularization(self):
        return condition(self.fc1)

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
            loss = loss_ce + loss_cr
            # mandatory report
            print('\t', colored('CE', 'blue'),
                    '%.5f'%loss_ce.item(), 'Acc', '%.3f'%acc_orig,
                    '|', colored('CR', 'red'),
                    '%.5f'%loss_cr.item())
            return (output, loss)
