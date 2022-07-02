import os
import argparse
import torch as th
import torch.nn.functional as F
from . import mnist_dataset
from torch.nn.utils.rnn import pack_padded_sequence, unpack_sequence
import rich
from rich.progress import track
from . import models
console = rich.get_console()


def train_one_epoch(model, optim, loader,
        *,
        epoch: int = -1,
        device: str = 'cpu',
        report_every: int = 50,
        logdir: str = None):
    '''
    train for one epoch, literally
    '''
    if logdir is not None:
        logfile = open(os.path.join(logdir, 'train_log.txt'), 'at')
    else:
        logfile = None
    for i, (x, y, z) in enumerate(loader):
        pack = pack_padded_sequence(x, z)
        pack = pack.to(device)
        y = y.to(device)
        logits = model(pack)
        #print(logits.shape, y.shape)
        loss = F.cross_entropy(logits, y, reduction='mean')
        optim.zero_grad()
        loss.backward()
        optim.step()

        if (i)%report_every == 0:
            pred = logits.max(dim=1)[1]
            acc = (pred == y).cpu().float().mean().item() * 100
            console.print(f'Eph[{epoch}] ({i+1}/{len(loader)})',
                    f'loss={loss.item():.3f}',
                    f'accuracy={acc:.2f} (/100)',
                    )
            if logfile is not None:
                logfile.write(f'Eph[{epoch}] ({i+1}/{len(loader)}) ')
                logfile.write(f'loss={loss.item():.3f} ')
                logfile.write(f'accuracy={acc:.2f} (/100)')
                logfile.write('\n')


@th.no_grad()
def evaluate(model, loader,
        *,
        epoch: int = -1,
        device: str = 'cpu',
        logdir: str = None,
        ):
    '''
    evaluate, literally
    '''
    if logdir is not None:
        logfile = open(os.path.join(logdir, 'evaluate_log.txt'), 'at')
    else:
        logfile = None
    losses = []
    preds = []
    ys = []
    for (x, y, z) in track(loader, description=f'Evaluation ...'):
        pack = pack_padded_sequence(x, z)
        pack = pack.to(device)
        y = y.to(device)
        logits = model(pack)
        loss = F.cross_entropy(logits, y, reduction='none')

        losses.append(loss)
        ys.append(y)
        preds.append(logits.max(dim=1)[1])
    losses = th.hstack(losses)
    preds = th.hstack(preds)
    ys = th.hstack(ys)
    #console.print(losses.shape, preds.shape, ys.shape)
    mean_loss = losses.mean()
    acc = (preds == ys).cpu().float().mean().item() * 100
    console.print(f'Eph[{epoch}] Evaluation:',
            f'loss={mean_loss:.2f}',
            f'acc={acc:.2f} (/100)')
    if logfile is not None:
        logfile.write(f'Eph[{epoch}] Evaluation: ')
        logfile.write(f'loss={mean_loss:.2f} ')
        logfile.write(f'acc={acc:.2f} (/100) ')
        logfile.write('\n')

        state_dict = model.state_dict()
        ptpath = os.path.join(logdir, f'model_eph_{epoch}.pt')
        th.save(state_dict, ptpath)
        console.print(f'Model state dictionary dumped to: {ptpath}')
