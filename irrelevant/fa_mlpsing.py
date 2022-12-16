import os
import torch as th
import collections
from . import fashion, base
import yaml
from tqdm import tqdm
from .attacks import projectedGradientDescent
from termcolor import cprint, colored
from . import fa_mlp
import torch.nn.functional as F


class Model(fa_mlp.Model):
    def forward_with_trace(self, x):
        i1 = x.view(-1, 28 * 28)
        i2 = F.relu(self.fc1(i1))
        i3 = F.relu(self.fc2(i2))
        logits = self.fc3(F.dropout(i3, p=0.4, training=self.training))
        return (i1, i2, i3, logits)

    def trace_to_ir(self, trace):
        # `trace` comes from self.forward_with_trace(...)
        (i1, i2, i3, logits) = trace
        # calculate ir
        ir1 = th.mm(i1, self.fc1.weight.T)
        ir2 = th.mm(i2, self.fc2.weight.T)
        ir3 = th.mm(i3, self.fc3.weight.T)
        return (ir1, ir2, ir3)

    def alir(self, iro, ira, *, ircoef: float = 1e-1):
        vo = th.cat([iro[0].ravel(), iro[1].ravel(), iro[2].ravel()]).detach()
        va = th.cat([ira[0].ravel(), ira[1].ravel(), ira[2].ravel()])
        return ircoef * th.mean(th.abs(va - vo))

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
                #output, loss = self.loss(images, labels, adv=False)
                trace_o = self.forward_with_trace(images)
                output = trace_o[-1]
                loss = F.cross_entropy(output, labels)
                acc_orig = (output.max(1)[1].eq(labels).sum().item()/len(y))
                loss_orig = loss.detach()
                iro = self.trace_to_ir(trace_o)
            # start PGD attack
            xr, r = projectedGradientDescent(self, images, labels,
                    eps=0.06, alpha=2./255., maxiter=12, verbose=False,
                    device=device, targeted=False, unbound=False)
            # forward the PGD adversary
            self.train()
            #output, loss = self.loss(xr, labels, adv=False)
            trace_a = self.forward_with_trace(xr)
            output = trace_a[-1]
            loss = F.cross_entropy(output, labels)
            acc_adv = (output.max(1)[1].eq(labels).sum().item()/len(y))
            loss_adv = loss.detach()
            ira = self.trace_to_ir(trace_a)
            # add ir loss
            irloss = self.alir(iro, ira)
            loss = loss + irloss
            # mandatory report
            print('\t', colored('Orig loss', 'blue'),
                    '%.5f'%loss_orig, 'Acc', '%.3f'%acc_orig,
                    '|', colored('[Adv loss]', 'red'),
                    '%.5f'%loss.item(), 'Acc', '%.3f'%acc_adv,
                    '|', colored('[IR loss]', 'yellow'),
                    '%.5f'%irloss.item())
            return (output, loss)
