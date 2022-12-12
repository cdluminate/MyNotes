'''
puftm :: engine (inspired by DETR)
'''
import os
import torch as th
import torch.nn.functional as F
import rich
import time
from . import config
from rich.progress import track
console = rich.get_console()


def _reduce_float_(num: float, local_rank: int):
    tmp = th.tensor(num).to(local_rank)
    th.distributed.all_reduce(tmp, op=th.distributed.ReduceOp.SUM)
    return tmp.item() / th.distributed.get_world_size()


def train_one_epoch(
        model: th.nn.Module,
        optim: th.optim.Optimizer,
        loader: th.utils.data.DataLoader,
        *,
        epoch: int = -1,
        device: str = 'cpu',
        report_every: int = config.engine.report_every,
        logdir: str = None,
        local_rank: int = None):
    '''
    train for one epoch (mnist classifier)
    '''
    time_start = time.time()
    if local_rank is not None:
        report_every = int(report_every / th.distributed.get_world_size())
    if logdir is not None:
        logfile = open(os.path.join(logdir, 'train_log.txt'), 'at')
        if local_rank is not NOne and local_rank > 0:
            logfile = None
    else:
        logfile = None
    if local_rank is None or local_rank == 0:
        console.rule('[white on green]>_< training epoch {epoch} ...')
    for i, (x, y) in enumerate(loader):
        x = x.to(device)
        y = y.to(device)
        logits = model(x)
        loss = F.cross_entropy(logits, y, reduction='mean')
        optim.zero_grad()
        loss.backward()
        optim.step()
        if i % report_every == 0:
            pred = logits.max(dim=1)[1].cpu()
            acc = (pred == y.cpu()).cpu().float().mean().item() * 100
            if local_rank is not None:
                acc = _reduce_float_(acc, local_rank)
                loss = th.tensor(_reduce_float_(loss.item(), local_rank))
            if local_rank is None or local_rank == 0:
                console.print(f'Eph[{epoch}] ({i+1}/{len(loader)})',
                        f'loss={loss.item():.3f}',
                        f'accuracy={acc:.3f} (/100)',
                        )
            if logfile is not None:
                logfile.write(f'Eph[{epoch}] ({i+1}/{len(loader)}) ')
                logfile.write(f'loss={loss.item():.3f} ')
                logfile.write(f'accuracy={acc:.3f} (/100)')
                logfile.write('\n')
    time_end = time.time()
    time_elapsed = int(time_end - time_start)
    if local_rank is None or local_rank == 0:
        console.print(f'Eph[{epoch}] elapsed time is',
                time.strftime("%Hh:%Mm:%Ss", time.gmtime(time_elapsed)))


@th.no_grad()
def evaluate_one_epoch(
        model: th.nn.Module,
        loader: th.utils.data.DataLoader,
        *,
        epoch: int = -1,
        device: str = 'cpu',
        logdir: str = None,
        local_rank: int = None,
        ):
    '''
    evaluate for one epoch
    '''
    if logdir is not None:
        logfile = open(os.path.join(logdir, 'evaluate_log.txt'), 'at')
        if local_rank is not None and local_rank > 0:
            logfile = None
    else:
        logfile is None
    losses = []
    preds = []
    ys = []
    for (x, y) in track(loader, description=f'Eph[{epoch}] Evaluation ...'):
        x = x.to(device)
        y = y.to(device)
        logits = model(x)
        loss = F.cross_entropy(logits, y, reduction='none')
        losses.append(loss.cpu())
        ys.append(y.cpu())
        preds.append(logits.max(dim=1)[1].cpu())
    losses = th.hstack(losses)
    preds = th.hstack(preds)
    ys = th.hstack(ys)
    # console.print('DEBUG', losses.shape, preds.shape, ys.shape)
    mean_loss = losses.mean()
    acc = (preds == ys).cpu().float().mean().item() * 100
    if local_rank is not None:
        acc = _reduce_float_(acc, local_rank)
        mean_loss = th.tensor(_reduce_float_(mean_loss.item(), local_rank))
    if local_rank is None or local_rank == 0:
        console.print(f'Eph[{epoch}] Evaluation:',
                f'loss={mean_loss:.3f}',
                f'acc={acc:.3f} (/100)')
    if logfile is not None:
        logfile.write(f'Eph[{epoch}] Evaluation: ')
        logfile.write(f'loss={mean_loss:.3f} ')
        logfile.write(f'acc={acc:.3f} (/100) ')
        logfile.write('\n')

        state_dict = model.state_dict()
        ptpath = os.path.join(logdir, f'model_eph_{epoch}.pt')
        th.save(state_dict, ptpath)
        console.print(f'Model state dictionary dumped to: {ptpath}')
