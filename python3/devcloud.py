#!/usr/bin/env python
import torch as th
import time
import torch
import torch.nn as nn
from torch.utils import mkldnn
from torch.utils.data import Dataset, DataLoader


def timeit(fun: callable):
    start = time.time()
    ret = fun()
    end = time.time()
    print(f'Elapsed {end - start} seconds')
    return ret

#        model.eval()
#        '''
#        1. User is suggested to use JIT mode to get best performance with DNNL with minimum change of Pytorch code. User may need to pass an explicit flag or invoke a specific DNNL optimization pass. The PyTorch DNNL JIT backend is under development (RFC link https://github.com/pytorch/pytorch/issues/23657), so the example below is given in imperative mode.
#        2. To have model accelerated by DNNL under imperative mode, user needs to explicitly insert format conversion for DNNL operations using tensor.to_mkldnn() and to_dense(). For best result, user needs to insert the format conversion on the boundary of a sequence of DNNL operations. This could boost performance significantly.
#        3. For inference task, user needs to prepack the model’s weight using mkldnn_utils.to_mkldnn(model) to save the weight format conversion overhead. It could bring good performance gain sometime for single batch inference.
#        '''
#        model_mkldnn = mkldnn.to_mkldnn(model)
#        for batch_index, data in enumerate(testLoader):
#            y = model_mkldnn(data.to_mkldnn())


def test_cpu():
    x = th.rand(4096, 4096)
    m = th.nn.Linear(4096, 4096)
    m.eval()
    with th.no_grad():
        for i in range(100):
            y = m(x)


def test_dnnl():
    x = th.rand(4096, 4096)
    x = x.to_mkldnn()
    m = th.nn.Linear(4096, 4096)
    m = mkldnn.to_mkldnn(m)
    m.eval()
    with th.no_grad():
        for i in range(100):
            y = m(x)

timeit(test_cpu)
timeit(test_dnnl)

