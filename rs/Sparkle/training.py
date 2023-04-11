import torch as th
import pytest


def lrSet(optim, lr: float) -> None:
    '''
    Set learning rate for the given optimizer.
    '''
    for param_group in optim.param_groups:
        param_group['lr'] = lr


@pytest.mark.parametrize('lr', [.1, 1.])
def test_lr_set(lr):
    l = th.nn.Linear(10, 10).cpu()
    optim = th.optim.Adam(l.parameters(), lr=1e-3)
    for param_group in optim.param_groups:
        assert(param_group['lr'] == 1e-3)
    lrSet(optim, lr)
    for param_group in optim.param_groups:
        assert(param_group['lr'] == lr)
