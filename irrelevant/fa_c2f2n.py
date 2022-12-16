import os
import torch as th
import collections
from . import fashion, common, base
import yaml
from tqdm import tqdm
from .attacks import projectedGradientDescent
from termcolor import cprint, colored
from . import classify
import random

class Model(base.Model):
    """
    LeNet-like convolutional neural network
    https://github.com/zalandoresearch/fashion-mnist/blob/master/benchmark/convnet.py
    """
    def __init__(self):
        super(Model, self).__init__()
        self.conv1a = th.nn.Conv2d(1, 32, kernel_size=5, padding=2)
        self.conv1b = th.nn.Conv2d(1, 32, kernel_size=5, padding=2)
        self.conv2a = th.nn.Conv2d(32, 64, kernel_size=5, padding=2)
        self.conv2b = th.nn.Conv2d(32, 64, kernel_size=5, padding=2)
        self.fc1a = th.nn.Linear(64*7*7, 1024)
        self.fc1b = th.nn.Linear(64*7*7, 1024)
        self.fc2 = th.nn.Linear(1024, 10)
        #def __copyto(m1, m2, neg=False):
        #    m2.weight.data.copy_(-m1.weight.data if neg else m1.weight.data)
        #    #m2.bias.data.copy_(-m1.bias.data if neg else m1.bias.data)
        #for (a,b) in zip((self.conv1a, self.conv2a, self.fc1a),
        #        (self.conv1b, self.conv2b, self.fc1b)):
        #    __copyto(a, b, neg=True)

    def forward_a(self, x):
        # -1, 1, 28, 28
        xa = th.nn.functional.relu(self.conv1a(x))
        ir1 = xa
        # -1, 32, 28, 28
        xa = th.nn.functional.max_pool2d(xa, kernel_size=2, stride=2)
        # -1, 32, 14, 14
        xa = th.nn.functional.relu(self.conv2a(xa))
        ir2 = xa
        # -1, 64, 14, 14
        xa = th.nn.functional.max_pool2d(xa, kernel_size=2, stride=2)
        # -1, 64, 7, 7
        xa = xa.view(-1, 64*7*7)
        # -1, 64*7*7
        xa = th.nn.functional.relu(self.fc1a(xa))
        ir3 = xa
        return (ir1, ir2, ir3)

    def forward_b(self, x):
        # -1, 1, 28, 28
        #xb = th.nn.functional.relu(self.conv1b(x))
        xb = th.clamp(self.conv1b(x), max=0.)
        ir1 = xb
        # -1, 32, 28, 28
        #xb = th.nn.functional.max_pool2d(xb, kernel_size=2, stride=2)
        xb = -th.nn.functional.max_pool2d(-xb, kernel_size=2, stride=2)
        # -1, 32, 14, 14
        #xb = th.nn.functional.relu(self.conv2b(xb))
        xb = th.clamp(self.conv2b(xb), max=0.)
        ir2 = xb
        # -1, 64, 14, 14
        #xb = th.nn.functional.max_pool2d(xb, kernel_size=2, stride=2)
        xb = -th.nn.functional.max_pool2d(-xb, kernel_size=2, stride=2)
        # -1, 64, 7, 7
        xb = xb.view(-1, 64*7*7)
        # -1, 64*7*7
        #xb = th.nn.functional.relu(self.fc1b(xb))
        xb = th.clamp(self.fc1b(xb), max=0.)
        ir3 = xb
        return (ir1, ir2, ir3)

    def forward(self, x, ir:bool=False):
        # -1, 1, 28, 28
        ir_a = self.forward_a(x)
        ir_b = self.forward_b(x)
        ir_ab = tuple(zip(ir_a, ir_b))
        x = (ir_a[-1] + ir_b[-1])/2.0  # neutralize
        x = th.nn.functional.dropout(x, p=0.1, training=self.training)
        # -1, 1024
        x = self.fc2(x)
        # return
        if ir:
            return (x, ir_ab)
        else:
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

    def loss(self, x, y, *, adv=True):  # note, adv is true
        device = self.fc1a.weight.device
        images, labels = x.to(device), y.to(device).view(-1)
        if not adv:
            output = self.forward(images)
            loss = th.nn.functional.cross_entropy(output, labels)
            return output, loss
        else: # toggle Nullspace defensive training (Mo Method)
            # utility function
            def flatcat(feats):
                return th.cat([x.view(x.shape[0], -1) for x in feats], dim=1)
            # CE(benign)
            self.train()
            output, ir = self.forward(images, ir=True)
            loss_ce = th.nn.functional.cross_entropy(output, labels)
            acc_orig = (output.max(1)[1].eq(labels).sum().item()/len(y))
            # PGD Attack
            self.eval()
            PGD_EPSILON=0.3
            xr, r = projectedGradientDescent(self, images, labels,
                    eps=PGD_EPSILON, alpha=2./255, maxiter=48, verbose=False,
                    device='cuda', targeted=False, unbound=False)
            # CE(adv)
            self.train()
            output_adv, loss_ce_adv = self.loss(xr, labels, adv=False)
            acc_adv = (output_adv.max(1)[1].eq(labels).sum().item()/len(y))
            # Nullspace / Duality loss
            ir_a = self.forward_a(xr)
            ir_b = self.forward_b(xr)
            if False:
                xpr = (images + r).clamp(min=0., max=1.)
                xmr = (images - r).clamp(min=0., max=1.)
                dice = random.random()
                output_a, ir_a = self.forward_a(xpr if dice < 0.5 else xmr, ir=True)
                output_b, ir_b = self.forward_b(xmr if dice < 0.5 else xpr, ir=True)
            loss_duality_euc = ((ir_a[2] - ir[2][0]) - (ir[2][1] - ir_b[2])).view(ir_a[2].shape[0],-1).norm(2,dim=1).mean()
            loss_nocollapse = (PGD_EPSILON-(ir_a[2]-ir[2][0]).view(ir_a[2].shape[0],-1).norm(2,dim=1).mean()).clamp(min=0.) + \
                    (PGD_EPSILON-(ir_b[2]-ir[2][1]).view(ir_b[2].shape[0],-1).norm(2,dim=1).mean()).clamp(min=0.)
            __cos = th.nn.functional.cosine_similarity
            loss_duality_cos = 1 + __cos((ir_a[2]-ir[2][0]).view(ir_a[2].shape[0],-1),
                (ir_b[2]-ir[2][1]).view(ir_b[2].shape[0],-1)).mean()
            loss = 0e-0*loss_ce + 1e-0*loss_ce_adv + 1e-1 * (loss_duality_euc + loss_duality_cos + loss_nocollapse)
            # mandatory report
            print(colored('|', 'magenta'),
                    colored('CE[Bng]', 'blue'), '%.5f'%loss_ce.item(),
                    colored('Acc[Bng]', 'green'), '%.3f'%acc_orig,
                    colored('CE[PGD]', 'blue'), '%.5f'%loss_ce_adv.item(),
                    colored('Acc[PGD]', 'green'), '%.3f'%acc_adv,
                    colored('Dual-Euc[PGD]', 'red'), '%.5f'%loss_duality_euc.item(),
                    colored('Dual-Cos[PGD]', 'red'), '%.5f'%loss_duality_cos.item(),
                    colored('NoCol[PGD]', 'red'), '%5f'%loss_nocollapse.item(),
                    )
            return (output, loss)
        if False: # toggle adversarial training (Madry Method)
            # baseline: forward original samples
            self.eval()
            with th.no_grad():
                output, loss = self.loss(images, labels, adv=False)
                acc_orig = (output.max(1)[1].eq(labels).sum().item()/len(y))
                loss_orig = loss.detach()
            # start PGD attack
            xr, r = projectedGradientDescent(self, images, labels,
                    eps=0.3, alpha=2./255., maxiter=48, verbose=False,
                    device='cpu', targeted=False, unbound=False)
            # forward the PGD adversary
            self.train()
            output, loss = self.loss(xr, labels, adv=False)
            acc_adv = (output.max(1)[1].eq(labels).sum().item()/len(y))
            loss_adv = loss.detach()
            # mandatory report
            print('\t', colored('Orig loss', 'blue'),
                    '%.5f'%loss_orig, 'Acc', '%.3f'%acc_orig,
                    '|', colored('[Adv loss]', 'red'),
                    '%.5f'%loss.item(), 'Acc', '%.3f'%acc_adv)
            return (output, loss)

    def report(self, epoch, iteration, total, output, labels, loss):
        result = classify.cls_report(output, labels, loss)
        print(f'Eph[{epoch}][{iteration}/{total}]', result)

    def validate(self, dataloader):
        device = self.fc1a.weight.device
        return classify.cls_validate(self, dataloader)

    def attack(self, att, loader, *, dconf, verbose=False):
        device = self.fc1a.weight.device
        return classify.cls_attack(self, att, loader,
                dconf=dconf, device=device, verbose=verbose)

    def neuroski(self, ski, loader, *, dconf, verbose=False):
        device = self.fc1a.weight.device
        return common.cls_neuroski(self, ski, loader,
                dconf=dconf, device=device, verbose=verbose)
