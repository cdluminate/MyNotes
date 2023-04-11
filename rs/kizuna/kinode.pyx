'''
Core Classes for kizuna Dynamic Computation Graph Engine
Copyright (C) 2018 Mo Zhou <cdluminate@gmail.com>
MIT License
'''
from typing import *
import numpy as np
cimport numpy as np


class kiNode(object):
    '''
    Single Node in a dynamic computation graph. In principal this is merely
    a tensor data container, which optionally holds a gradient tensor.
    '''

    def __init__(self, data: Any, *, rg = True):
        '''
        Instantiate a single node in the computation graph. Note that the
        connections between the nodes aren't recorded by this class.

        Args:
            data (np.ndarray or list or tuple): ...
            rg (bool): does this node require gradient?
        '''
        if isinstance(data, np.ndarray):
            self.data = data
        elif isinstance(data, list) or isinstance(data, tuple):
            self.data = np.array(data)
        else:
            raise TypeError(f'Type {type(data)} not supported')
        self.rg = rg
        self.grad = np.zeros_like(self.data)  # let's waste some memor
        self.operator = None
        self.operands = None


    def __repr__(self):
        return f'''kiNode(shape={self.data.shape}, rg={'✓' if self.rg else '✗'}, op={self.operator},
       data=\n{self.data},'''  + (f'''
       grad=\n{self.grad})''' if (self.grad**2).sum()>1e-9 else '')


    def reset(self, value=0):
        '''
        Reset the gradient tensor to zero array.
        '''
        self.grad[:] = value


    def zeroGrad(self):
        if self.rg:
            self.grad[:] = 0
            if self.operands is not None:
                for node in self.operands['inp']:
                    if node.rg: node.zeroGrad()


    def backward(self, *, toplevel=True):
        #print(hex(id(self)), '.backward(...)')
        if self.rg and self.operator is not None:
            if toplevel:
                self.reset(1)
            self.operator(**self.operands)
            for node in self.operands['inp']:
                node.backward(toplevel=False)


    def update(self, recursive: bool= True, *, lr=1e-3):
        #print(hex(id(self)), '.update(...)')
        if self.rg:
            self.data -= lr * self.grad
            if self.operator is None: return
            for node in self.operands['inp']:
                node.update(recursive=True, lr=lr)


    def __copy__(self):
        '''
        Copy myself into a new kiNode.
        '''
        def _copy_backward(*, inp: tuple, out: tuple) -> None:
            if inp[0].rg: inp[0].grad += out[0].grad
        n = kiNode(np.copy(self.data))
        n.operator = _copy_backward
        n.operands = {'inp': (self,), 'out': (n,)}
        return n


    def __add__(self, friend):
        '''
        Add two tensors together. Their shape must be the same.
        '''
        def _add_backward(*, inp: tuple, out: tuple) -> None:
            if inp[0].rg: inp[0].grad += out[0].grad
            if inp[1].rg: inp[1].grad += out[0].grad
        n = kiNode(self.data + friend.data)
        n.operator = _add_backward
        n.operands = {'inp': (self, friend), 'out': (n,)}
        return n


    def __sub__(self, friend):
        def _sub_backward(*, inp: tuple, out: tuple) -> None:
            if inp[0].rg: inp[0].grad += out[0].grad
            if inp[1].rg: inp[1].grad -= out[0].grad
        n = kiNode(self.data - friend.data)
        n.operator = _sub_backward
        n.operands = {'inp': (self, friend), 'out': (n,)}
        return n


    def __pow__(self, num: int):
        def _pow_backward(*, num: int, inp: tuple, out: tuple) -> None:
            if inp[0].rg: inp[0].grad += num * inp[0].data**(num-1) * out[0].grad
        n = kiNode(self.data ** num)
        n.operator = _pow_backward
        n.operands = {'num': num, 'inp': (self,), 'out': (n,)}
        return n


    def __sum__(self):
        '''
        sum: (d1, d2, ..., dn) -> (1,)
        '''
        def _sum_backward(*, inp: tuple, out: tuple) -> None:
            if inp[0].rg: inp[0].grad += out[0].grad
        n = kiNode(self.data.sum(keepdims=True))
        n.operator = _sum_backward
        n.operands = {'inp': (self,), 'out': (n,)}
        return n


    def __abs__(self):
        '''
        abs: (d1, d2, ..., dn) -> (d1, d2, ..., dn)
        '''
        def _abs_backward(*, inp: tuple, out: tuple) -> None:
            if inp[0].rg: inp[0].grad += ((self.data>1e-16)*1 + (self.data<-1e-16)*-1)*out[0].grad
        n = kiNode(np.abs(self.data))
        n.operator = _abs_backward
        n.operands = {'inp': (self,), 'out': (n,)}
        return n


    def __gemm__(self, friend):
        '''
        gemm: (m, k) x (k, n) -> (m, n)
        '''
        def _gemm_backward(*, inp: tuple, out: tuple) -> None:
            if inp[0].rg: inp[0].grad += out[0].grad @ inp[1].data.T
            if inp[1].rg: inp[1].grad += inp[0].data.T @ out[0].grad
        n = kiNode(self.data @ friend.data)
        n.operator = _gemm_backward
        n.operands = {'inp': (self, friend), 'out': (n,)}
        return n


    def __softmax__(self, dim):
        '''
        softmax: (m, n) -> (m, n)
        '''
        def _softmax_backward(*, dim: int, inp: tuple, out: tuple) -> None:
            if inp[0].rg:
                batch = inp[0].data.shape[[1,0].index(dim)]
                datadim = inp[0].data.shape[dim]
                for i in range(batch):
                    if dim == 0:
                        y = out[0].data[:, i]
                    else:
                        y = out[0].data[i, :]
                    jacob = np.diag(y)
                    jacob -= y.reshape(datadim, 1) @ y.reshape(1, datadim)
                    if dim == 0:
                        g = jacob @ out[0].grad[:, i]
                        inp[0].grad[:, i] += g.reshape(inp[0].grad[:,i].shape)
                    else:
                        g = jacob @ out[0].grad[i, :]
                        inp[0].grad[i, :] += g.reshape(inp[0].grad[i,:].shape)
        x = np.exp(self.data - self.data.max(dim, keepdims=True))
        x = x / x.sum(dim, keepdims=True)
        n = kiNode(x)
        n.operator = _softmax_backward
        n.operands = {'dim': dim, 'inp': (self,), 'out': (n,)}
        return n


    def __nll__(self, dim, label):
        '''
        nll: (m, n) x [(n,)|(m,)] -> [(m,)|(n,)]
        '''
        label.data = label.data.flatten()
        def _nll_backward(*, dim: int, inp: tuple, out: tuple) -> None:
            if inp[0].rg and dim == 0:
                g = 1 / inp[0].data[label.data,
                        list(range(inp[0].data.shape[1]))]
                inp[0].grad[label.data,
                        list(range(inp[0].data.shape[1]))] = g
            if inp[0].rg and dim == 1:
                g = 1 / inp[0].data[list(range(inp[0].data.shape[1])),
                        label.data]
                inp[0].grad[list(range(inp[0].data.shape[1])),
                        label.data] = g
        if dim == 0:
            x = - np.log(self.data[label.data, list(range(self.data.shape[1]))])
        else:
            x = - np.log(self.data[list(range(self.data.shape[0])), label.data])
        n = kiNode(x)
        n.operator = _nll_backward
        n.operands = {'dim': dim, 'inp': (self, label), 'out': (n,)}
        return n


    def __collapse__(self, shape):
        raise NotImplementedError


    def __expand__(self, shape):
        raise NotImplementedError
