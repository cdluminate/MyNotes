import functools as ft
import math
import numpy as np
import os
import sys
import re
import random
import statistics
import torch as th
import torch.nn.functional as F
import torchvision as V
import gc
import fcntl
from scipy.optimize import curve_fit
import json
import rich
from rich.progress import track
console = rich.get_console()


def BIM_l8_T(model, images, labels, *, eps=8./255., alpha=2./255., maxiter=6, verbose=False):
    '''
    model should have the classification head.
    the images are always in [0, 1].
    the images are using imagenet normalizations.
    '''
    model.eval()
    device = images.device
    images_orig = images.clone().detach()
    labels_orig = labels.clone().detach()
    images = images.clone().detach()
    traj = [images_orig.clone().detach()]
    batch_size = images.shape[0]
    for _ in range(maxiter):
        images.requires_grad = True
        outputs = model.forward(images)
        loss = F.cross_entropy(outputs, labels)
        if verbose:
            console.print('>', 'loss', loss.item())
        grad = th.autograd.grad(loss, images,
                                retain_graph=False,
                                create_graph=False)[0]
        images = images.detach() + alpha * grad.sign()
        diff = th.clamp(images - images_orig, min=-eps, max=+eps).detach()
        images = th.clamp(images_orig + diff, min=0., max=1.).detach()
        traj.append(images.clone().detach())
    traj = th.stack(traj)
    return traj


def traj2arcm(model, traj, Nclass:int=1000):
    model.eval()
    device = traj.device
    assert len(traj.shape) == 5
    Nstep = traj.shape[0]
    Nbatch = traj.shape[1]
    Nflatten = traj.shape[2] * traj.shape[3] * traj.shape[4]
    arcM = []
    def _jx_from_jacobian(isample):
        Jx = []
        for istep in track(range(Nstep), description=f'ARC-M[{isample+1}/{Nbatch}]'):
            gc.collect()
            #console.print('arcM> isample', isample, 'istep', istep+1, '/', Nstep)
            xi = traj[istep, isample, :, :, :]  # [1, 1, C, H, W]
            if len(xi.shape) == 3:
                xi = xi.unsqueeze(0)  # [1, C, H, W]
            jxi = th.autograd.functional.jacobian(model, xi, create_graph=False)
            # [D, 1, C, H, W]
            jxi = jxi.view(-1).clone().detach().cpu().to(th.float32)
            Jx.append(jxi)
        return Jx
    for isample in range(Nbatch):
        gc.collect()
        Jx = _jx_from_jacobian(isample)
        lock = open('/dev/shm/X-arcm-prevent-oom.lock', 'w')
        fcntl.lockf(lock, fcntl.LOCK_EX)
        with th.no_grad():
            tmp = []
            for k in range(Nclass):
                Jxk = th.stack([x[k*Nflatten:(k+1)*Nflatten] for x in Jx])
                Jxkn = th.nn.functional.normalize(Jxk)
                cos = th.mm(Jxkn, Jxkn.T)
                tmp.append(cos.clone().detach().cpu())
            sums = [x.sum().item() for x in tmp]
            argsort = np.argsort(sums)[::-1]
            tmp = tmp[argsort[0]]
            tmp = [tmp]
        arcM.append(th.stack(tmp).mean(0).detach())
        fcntl.lockf(lock, fcntl.LOCK_UN)
        lock.close()
    arcM = np.vstack([x.cpu().numpy().reshape(1, -1) for x in arcM])
    arcM = arcM.reshape(arcM.shape[0], Nstep, Nstep)
    return arcM


def arcm2v(arcm: np.ndarray) -> np.ndarray:
    def laplace(x, *p):
        A, scale = p
        return A * np.exp(-np.abs(x/scale))
    if len(arcm.shape) == 2:
        assert arcm.shape[0] == arcm.shape[1]
        n = arcm.shape[0]
        mr = np.arange(n).reshape(n, 1).repeat(n, axis=1)
        mc = np.arange(n).reshape(1, n).repeat(n, axis=0)
        x = np.abs(mr - mc).reshape(-1)
        y = arcm.reshape(-1)
        coef, var_matrix = curve_fit(laplace, x, y,
            p0=[1.0, 1.0], method='lm')
        return coef
    elif len(arcm.shape) == 3:
        batchsize = arcm.shape[0]
        coefs = np.stack([arcm2v(m) for m in arcm])
        return coefs
    else:
        raise ValueError(f'arcm shape {arcm.shape} is illegal')


if __name__ == '__main__':
    #model = V.models.resnet18(weights=V.models.ResNet18_Weights.DEFAULT)
    model = V.models.resnet18(weights=None)
    model.fc = th.nn.Linear(512, 10)
    batchsize = 2
    images = th.rand(batchsize, 3, 224, 224)
    labels = th.randint(0, 10, (batchsize,))
    traj = BIM_l8_T(model, images, labels, verbose=True)
    print(traj.shape)
    cos = traj.view(traj.shape[0], -1)
    cos = F.normalize(cos)
    cos = 1.0 - th.cdist(cos, cos)
    print(cos.shape, cos)
    arcm = traj2arcm(model, traj, Nclass=10)
    print(arcm.shape, arcm)
    arcv = arcm2v(arcm)
    print(arcv.shape, arcv)
    console.print('[red]averaged test outputs')
    arcv = arcv.mean(axis=0)
    print(arcv)
