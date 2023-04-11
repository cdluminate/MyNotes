#!/usr/bin/python3
import numpy as np
import kizuna as ai
import pytest


@pytest.mark.parametrize('size', [1, 2, 4, 8, 128])
def test_quadratic_eltwise(size):
    w = ai.kiNode(np.eye(size)*2)
    for i in range(300):
        y = w ** 2
        y.zeroGrad()
        y.backward()
        y.update(lr=1e-1)
    assert(w.data.sum() < 1e-16)


@pytest.mark.parametrize('size', [1, 2, 4, 8, 128])
def test_norm2_eltwise(size):
    w1 = ai.kiNode(np.eye(size)*3.2)
    w2 = ai.kiNode(np.eye(size)*3.2)
    t = ai.kiNode(np.eye(size), rg=False)
    for i in range(300):
        y1 = abs(w1 - t).__pow__(2).__sum__()
        y1.zeroGrad()
        y1.backward()
        y1.update(lr=1e-1)

        y2 = abs(t - w2).__pow__(2).__sum__()
        y2.zeroGrad()
        y2.backward()
        y2.update(lr=1e-1)
    assert(np.abs(w1.data - t.data).sum() < 1e-8)
    assert(np.abs(w2.data - t.data).sum() < 1e-8)


@pytest.mark.parametrize('s', [(1,1,1), (1,2,1), (5,5,5), (5,3,5), (5,7,5), (5,5,3), (3,5,5)])
def test_gemm_backward(s):
    x = ai.rand((s[0], s[1]))
    y = ai.ones((s[1], s[2]))
    z = x.__gemm__(y)
    z.zeroGrad()
    z.backward()


@pytest.mark.parametrize('s', [1, 2, 4, 8, 128])
def test_linear_system(s):
    x = ai.eye(s)
    x.rg = False
    y = ai.rand((s,s))
    z = ai.eye(s)
    z.rg = False
    for i in range(300):
        zp = x.__gemm__(y)
        l = abs(zp - z).__pow__(2).__sum__()
        l.zeroGrad()
        l.backward()
        l.update(lr=1e-1)
    assert(((y.data - z.data)**2).sum() < 1e-9)


def test_softmax_dim1():
    x = ai.node(np.array([[1,2,3], [2,3,1]], dtype=np.float64))
    y = x.__softmax__(1)
    y.zeroGrad()
    y.backward()
    #print('y', y)
    #print('x', x)
    #print('real jacob 0', np.diag(y.data[0]) - y.data[0].reshape(3,1)@y.data[0].reshape(1,3))
    #print('real jacob 1', np.diag(y.data[1]) - y.data[1].reshape(3,1)@y.data[1].reshape(1,3))
