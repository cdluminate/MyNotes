'''
Adversarial Perturbation Decomposition
'''
import torch as th
import numpy as np


class _UntargetDecomp(th.nn.Module):

    def __init__(self, dim: int, ncls: int, eps: float):
        self.dim = dim
        self.ncls = ncls
        self._carrier = th.nn.Parameter(th.randn(dim))
        self._payload = th.nn.Embedding(ncls, dim)
        self._xi = th.nn.Parameter(th.tensor(0.5))

    def perturbs(self, x, y):
        # generate carrier
        carrier = self._epsilon * self._xi * th.sin(self._carrier) / 2.0
        carrier = carrier.view(1, -1).repeat(x.size(0), 1)
        # generate payload
        payload = self._payload(y)
        payload = self._epsilon * (1-self._xi) * th.sin(payload) / 2.0
        # combine and return
        return carrier + payload


class _CoarseDecomp(th.nn.Module):

    def __init__(self, dim: int, ncls: int, eps: float):
        self.dim = dim
        self.ncls = ncls
        self._carrier = th.nn.Parameter(th.randn(dim))
        self._payload = th.nn.Embedding(ncls, dim)
        self._xi = th.nn.Parameter(th.tensor(0.5))
        self._epsilon = eps

    def perturbs(self, x, y):
        # generate carrier
        carrier = self._epsilon * self._xi * th.sin(self._carrier) / 2.0
        carrier = carrier.repeat(x.size(0) * self.ncls, 1, 1, 1)
        # generate payload
        rhos = self._payload(th.arange(self.ncls))
        payload = self._epsilon * (1-self._xi) * th.sin(rhos) / 2.0
        payload = payload.repeat(x.size(0), 1, 1, 1)
        # combine and return
        return carrier + payload

    def forward(self, x, y):
        ptbs = self.perturbs().view(1, *x.shape[1:])
        tildex = (x + ptbs).clamp(min=1e-7, max=1-1e-7)
        return tildex


class _FineDecomp(th.nn.Module):

    def __init__(self, dim: int, ncls: int, eps: float):
        self.dim = dim
        self.ncls = ncls
        self._carrier = th.nn.Embedding(ncls, dim)
        self._payload = th.nn.Embedding(ncls ** 2, dim)
        self._xi = th.nn.Parameter(th.tensor(0.5))
        self._epsilon = eps

    def perturbs(self, x, y):
        # generate carrier
        Cy = self._carrier[y]
        carrier = self._epsilon * self._xi * th.sin(Cy) / 2.0
        selector_c = th.arange(x.size(0)).view(
            x.size(0), 1).repeat(1, self.ncls).flatten()
        carrier = carrier[selector_c]
        # generate payloads
        selector_p = th.arange(self.ncls).repeat(x.size(0)) + \
            th.tensor(y).view(-1, 1).repeat(1, self.ncls).flatten()
        Pyt = self._payload[selector_p]
        payload = self._epsilon * (1-self._xi) * th.sin(Pyt) / 2.0
        # combine and return
        return carrier + payload

    def forward(self, x, y):
        ptbs = self.perturbs().view(1, *x.shape[1:])
        tildex = (x + ptbs).clamp(min=1e-7, max=1-1e-7)
        return tildex


class AdvDecomp(object):

    def __init__(self, model: th.nn.Module, variant: str, device: str):
        assert(variant in ('coarse', 'fine', 'untarget'))
        self.granularity = variant
        self.model = model
        self.device = device
        self.initialized = False
        decomposers = {'coarse': _CoarseDecomp,
                'fine': _FineDecomp,
                'untarget': _UntargetDecomp,
                }
        self.dim = 1024
        self.ncls = 10
        self.eps = 16./255.
        self.decomposer = decomposers[variant](
                self.dim, self.ncls, self.eps)

    def process_batch
