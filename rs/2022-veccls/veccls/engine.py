import os
import argparse
import torch as th
import torch.nn.functional as F
import rich
import time
from rich.progress import track
console = rich.get_console()

def _reduce_float_(num: float, local_rank: int):
    tmp = th.tensor(num).to(local_rank)
    th.distributed.all_reduce(tmp, op=th.distributed.ReduceOp.SUM)
    return tmp.item() / th.distributed.get_world_size()

def train_one_epoch(model, optim, loader,
        *,
        epoch: int = -1,
        device: str = 'cpu',
        report_every: int = 50,
        logdir: str = None,
        local_rank: int = None):
    '''
    train for one epoch, literally
    '''
    time_start = time.time()
    if local_rank is not None:
        report_every = int(report_every / th.distributed.get_world_size())
    if logdir is not None:
        logfile = open(os.path.join(logdir, 'train_log.txt'), 'at')
        if local_rank is not None and local_rank > 0:
            logfile = None
    else:
        logfile = None
    if local_rank is None or local_rank == 0:
        console.rule(f'[white on green]>_< training epoch {epoch} ...')
    for i, (x, y, trco, lens, packlens) in enumerate(loader):
        logits = model(x, y, trco, lens, packlens, device=device)
        #print(logits.shape, y.shape)
        loss = F.cross_entropy(logits, y.to(device), reduction='mean')
        optim.zero_grad()
        loss.backward()
        optim.step()

        if i%report_every == 0:
            pred = logits.max(dim=1)[1].cpu()
            acc = (pred == y.cpu()).cpu().float().mean().item() * 100
            if local_rank is not None:
                acc = _reduce_float_(acc, local_rank)
                loss = th.tensor(_reduce_float_(loss.item(), local_rank))
            if local_rank is None or local_rank == 0:
                console.print(f'Eph[{epoch}] ({i+1}/{len(loader)})',
                        f'loss={loss.item():.3f}',
                        f'accuracy={acc:.2f} (/100)',
                        )
            if logfile is not None:
                logfile.write(f'Eph[{epoch}] ({i+1}/{len(loader)}) ')
                logfile.write(f'loss={loss.item():.3f} ')
                logfile.write(f'accuracy={acc:.2f} (/100)')
                logfile.write('\n')
    time_end = time.time()
    time_elapsed = int(time_end - time_start)
    if local_rank is None or local_rank == 0:
        console.print(f'Eph[{epoch}] elapsed time',
                time.strftime("%Hh:%Mm:%Ss", time.gmtime(time_elapsed)))


@th.no_grad()
def evaluate(model, loader,
        *,
        epoch: int = -1,
        device: str = 'cpu',
        logdir: str = None,
        local_rank: int = None,
        ):
    '''
    evaluate, literally
    '''
    if logdir is not None:
        logfile = open(os.path.join(logdir, 'evaluate_log.txt'), 'at')
        if local_rank is not None and local_rank > 0:
            logfile = None
    else:
        logfile = None
    losses = []
    preds = []
    ys = []
    for (x, y, trco, lens, packlens) in track(loader, description=f'Evaluation ...'):
        logits = model(x, y, trco, lens, packlens, device=device)
        loss = F.cross_entropy(logits, y.to(device), reduction='none')

        losses.append(loss.cpu())
        ys.append(y.cpu())
        preds.append(logits.max(dim=1)[1].cpu())
    losses = th.hstack(losses)
    preds = th.hstack(preds)
    ys = th.hstack(ys)
    #console.print(losses.shape, preds.shape, ys.shape)
    mean_loss = losses.mean()
    acc = (preds == ys).cpu().float().mean().item() * 100
    if local_rank is not None:
        acc = _reduce_float_(acc, local_rank)
        mean_loss = th.tensor(_reduce_float_(mean_loss.item(), local_rank))
    if local_rank is None or local_rank == 0:
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
