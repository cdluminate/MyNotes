import argparse
import os
import numpy as np
import torch as th
import torch.nn.functional as F
import torchvision as V
import rich
from rich.progress import track
console = rich.get_console()
# in the current directory
import ilsvrc


def remove_prefix_from_state_dict(state_dict, prefix) -> dict:
    new_dict = {}
    for (k, v) in state_dict.items():
        mangled_name = k.replace(prefix, '')
        new_dict[mangled_name] = v
    return new_dict


class AverageMeter(object):
    '''
    Simplified meter (ref: train_imagenet.py)
    '''
    def __init__(self, name, fmt=':.3f'):
        self.name, self.fmt = name, fmt
        self.reset()
    def reset(self):
        self.val, self.avg, self.sum, self.count = (0, 0, 0, 0)
    def update(self, val, n=1):
        self.val, self.sum, self.count = (val, self.sum + val * n, self.count + n)
        self.avg = self.sum / self.count
    def __str__(self):
        fmtstr = '{name} {val' + self.fmt + '} ({avg' + self.fmt + '})'
        return fmtstr.format(**self.__dict__)
    def summary(self):
        fmtstr = '{name} {avg' + self.fmt + '} ({count' + self.fmt + '} samples)'
        return fmtstr.format(**self.__dict__)


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--datadir', type=str, default='./ILSVRC')
    ag.add_argument('--arch', type=str, default='resnet50')
    ag.add_argument('--batch', type=int, default=128)
    ag.add_argument('--resume', type=str, default='', help='path to pretrained weights')
    ag.add_argument('--device', type=str, default='cuda' if th.cuda.is_available() else 'cpu')
    ag = ag.parse_args()
    console.log(ag)

    console.log(f'>_< Initializing {ag.arch} ...')
    model = getattr(V.models, ag.arch)()
    #console.print(model)

    assert os.path.exists(ag.resume)
    console.log(f'>_< Loading {ag.resume} ...')
    checkpoint = th.load(ag.resume)
    state_dict = remove_prefix_from_state_dict(checkpoint['state_dict'], 'module.')
    model.load_state_dict(state_dict)
    del checkpoint
    model = model.to(ag.device)
    model.eval()

    console.log(f'>_< Loading validation set from {ag.datadir}')
    val_dataset = ilsvrc.ILSVRC(ag.datadir, 'val')
    val_loader = th.utils.data.DataLoader(val_dataset,
        batch_size=ag.batch, shuffle=False, num_workers=8,
        pin_memory=True, sampler=None)

    console.log('>_< Validate')
    acc1meter = AverageMeter('Acc@1', ':6.2f')
    acc5meter = AverageMeter('Acc@5', ':6.2f')
    for i, (images, labels) in track(enumerate(val_loader), total=len(val_loader)):
        images = images.to(ag.device)
        labels = labels.to(ag.device)

        images = ilsvrc.NORMALIZE(images)
        output = model(images)

        _, pred = output.topk(5, 1, True, True)
        pred = pred.t()
        correct = pred.eq(labels.view(1, -1).expand_as(pred))
        res = []
        for k in (1, 5):
            correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / labels.size(0)))
        acc1, acc5 = res
        console.log(f'Batch[{i:4d}]', acc1meter, acc5meter)
        acc1meter.update(acc1.item(), images.size(0))
        acc5meter.update(acc5.item(), images.size(0))

    console.log('Overall Evaluation Results is:')
    console.log(acc1meter.summary(), acc5meter.summary())
