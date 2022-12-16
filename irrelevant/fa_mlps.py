import os
import torch as th
import torch.nn.functional as F
import collections
from . import fashion, base
import yaml
from tqdm import tqdm
from .attacks import projectedGradientDescent
from termcolor import cprint, colored
from . import fa_mlp
from . import spre

class Model(fa_mlp.Model):

    def __init__(self, wants_teacher=False):
        '''
        wants_teacher: distillation with spectrum regularization

        Teacher method: worse than pure DSR
        '''
        super(Model, self).__init__()
        self.wants_teacher = wants_teacher
        device = self.fc1.weight.device

        if self.wants_teacher:
            self.teacher = fa_mlp.Model().to(device)
            path_stdict = os.path.join('trained', 'fa_mlp.sdth')
            self.teacher.load_state_dict(th.load(path_stdict))
            self.teacher.eval()

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
            output, loss_ce = self.loss(images, labels, adv=False)
            acc_orig = (output.max(1)[1].eq(labels).sum().item()/len(y))
            # CR, Zeta
            loss_cr = self.condition_regularization()
            loss_zt = spre.zeta(output)
            # sum
            loss = loss_ce + 1.0*loss_cr  # + 1.0*loss_zt
            # Teacher Representation Imitation
            if self.wants_teacher:
                with th.no_grad():
                    self.teacher.eval()
                    output_ref = self.teacher.forward(images)
                loss_te = F.pairwise_distance(output, output_ref).mean()
                loss = loss + loss_te/4.0
            else:
                loss_te = th.tensor(-1)
            #with th.no_grad():
            #    svd = th.svd(output)
            #    print(svd.S.max().item(), svd.S.min().item())
            # mandatory report
            print('\t', colored('CE', 'blue'),
                    '%.5f'%loss_ce.item(), 'Acc', '%.3f'%acc_orig,
                    '|', colored('CR', 'red'),
                    '%.5f'%loss_cr.item(),
                    'Zt', '%.5f'%loss_zt.item(),
                    'Te', '%.5f'%loss_te.item(),
                    )
            return (output, loss)
