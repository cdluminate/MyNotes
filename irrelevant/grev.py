# Copyright (C) 2022 Mo Zhou <cdluminate@gmail.com>
# License: AGPL-3.0
import torch as th
import numpy as np
from .utils import *
import rich
c = rich.get_console()

def grev(model, x0, label,
        thres: float = 0.8,
        alpha: float = 2./255.,
        epsilon: float = 8./255.,
        nomax: bool = False) -> th.Tensor:
    # shape
    if x0.size(1) == 1 and x0.size(2) == 28 and x0.size(3) == 28:
        epsilon = 77/255
    # calculate for step 0
    model.eval()
    with th.no_grad():
        out0 = model.forward(x0)  # 7,4
        pred0 = out0.max(1)[1]
    j0 = th.autograd.functional.jacobian(model, x0)  # 7,4,7,16
    #print('J0', j0.shape)
    if len(j0.shape) == 4 and not nomax:
        pyipx0 = j0[range(j0.size(0)), pred0, range(j0.size(0)), :]  # 7,16
    elif len(j0.shape) == 6 and not nomax:
        pyipx0 = j0[range(j0.size(0)), pred0, range(j0.size(0)), :, :, :]
        pyipx0 = pyipx0.view(pred0.size(0), -1)
        #print(pyipx0.shape)
    elif len(j0.shape) == 6 and nomax:
        pyipx0 = j0.mean(dim=1).view(pred0.size(0), -1)
    else:
        raise NotImplementedError
    #print(pyipx.shape)
    x = x0.clone().detach()
    for istep in range(int(1.5 * epsilon / alpha)):
        x = x - alpha * th.sign(pyipx0).reshape_as(x)
        # clip
        if x0.min() >= 0. and x0.max() <= 1.:
            x = th.min(x, x0 + epsilon)
            x = th.max(x, x0 - epsilon)
            x = th.clamp(x, min=0., max=1.)
        elif x0.min() < 0.:
            x = th.min(x, x0 + (epsilon/IMstd[:,None,None]).to(x.device))
            x = th.max(x, x0 - (epsilon/IMstd[:,None,None]).to(x.device))
            x = th.max(x, renorm(th.zeros(x.shape, device=x.device)))
            x = th.min(x, renorm(th.ones(x.shape, device=x.device)))
        else:
            raise NotImplementedError
        with th.no_grad():
            pred = model.forward(x).max(1)[1].item()
        j = th.autograd.functional.jacobian(model, x)
        if len(j.shape) == 4 and not nomax:
            pyipx = j[range(j.size(0)), pred, range(j.size(0)), :]
        elif len(j.shape) == 6 and not nomax:
            pyipx = j[range(j.size(0)), pred, range(j.size(0)), :, :, :]
            pyipx = pyipx.view(1, -1)
        elif len(j.shape) == 6 and nomax:
            pyipx = j.mean(dim=1).view(1, -1)
        else:
            raise NotImplementedError
        cos = th.nn.functional.cosine_similarity(pyipx, pyipx0).item()
        l1 = (x - x0).abs().sum().item()
        linf = (x - x0).abs().max().item()
        print(f'GREV[{istep:02d}]', 'COS', cos, 'L1', l1, 'Linf', linf)
        print(f'        ', 'Orig', label.item(), 'Adv', pred0.item(),
                'nowPRED', pred)
        if cos <= thres:
            break
    return x.clone().detach()


if __name__ == '__main__':
    # simpel test case
    model = th.nn.Sequential(
            th.nn.Linear(16, 10),
            th.nn.ReLU(),
            th.nn.Linear(10, 4),
            )
    print(model)
    inp = th.rand(1, 16)
    xrT = grev(model, inp)
