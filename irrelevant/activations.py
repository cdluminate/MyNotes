import torch as th
import numpy as np
import matplotlib.pyplot as plt

def surgery(model, srcCls, dstCls) -> th.nn.Module:
    # https://forums.fast.ai/t/change-activation-function-in-resnet-model/78456
    for (name, module) in reversed(model._modules.items()):
        if len(tuple(module.children())) > 0:
            model._modules[name] = surgery(module, srcCls, dstCls)
        if isinstance(module, srcCls):
            model._modules[name] = dstCls()
    return model

def test_surgery():
    import torchvision as vision
    model = vision.models.resnet18()
    model.add_module('test', th.nn.ReLU())
    print(model)
    surgery(model, th.nn.ReLU, SawSin)
    print(model)

class SawSin(th.nn.Module):
    def forward(self, x):
        return sawsin(x)

def sawsin(x):
    # saw-sin activation
    P = 2 * np.pi
    with th.no_grad():
        K = (x / P).int()
    rx = x - (K * P)
    mask_neg = (x < 0.0)
    mask_seg1 = th.logical_and(rx >= 0.0, rx < P/4)
    mask_seg23 = th.logical_and(rx >= P/4, rx < 3*P/4)
    mask_seg4 = th.logical_and(rx >= 3*P/4, rx < P)
    result = (mask_neg * 0.0)
    result = result + (mask_seg1 * (rx * (4/P)))
    result = result + (mask_seg23 * (2 - rx * (4/P)))
    result = result + (mask_seg4 * (-4 + rx * (4/P)))
    return result

class HSin(th.nn.Module):
    def forward(self, x):
        return hsin(x)

def hsin(x):
    # heaviside sin
    return th.heaviside(x, th.tensor(0.)) * th.sin(x)

def test_sawsin():
    import timeit
    N = 10000
    def _worker_sawsin():
        x = th.rand(1024)
        y = sawsin(x)
    def _worker_hsin():
        x = th.rand(1024)
        y = hsin(x)
    def _worker_relu():
        x = th.rand(1024)
        y = th.relu(x)
    t = timeit.timeit(_worker_relu, number=N)
    print('relu', t)
    t = timeit.timeit(_worker_sawsin, number=N)
    print('sawsin', t)
    t = timeit.timeit(_worker_hsin, number=N)
    print('hsin', t)

def sawsinabs(x):
    return sawsin(x).abs()

def sawcos(x):
    # saw-cos activation
    with th.no_grad():
        K = (x / (2 * np.pi)).int()
    rx = x - (2 * K * np.pi)
    mask_neg = (x < 0.0)
    mask_seg12 = th.logical_and(rx >= 0.0, rx < np.pi)
    mask_seg34 = th.logical_and(rx >= np.pi, rx < 2*np.pi)
    result = (mask_neg * 0.0)
    result = result + (mask_seg12 * (1 - rx * 2/np.pi))
    result = result + (mask_seg34 * (-3 + rx * 2/np.pi))
    return result

def slash(x):
    # slash activation
    with th.no_grad():
        K = (x / (2 * np.pi)).int()
    rx = x - (2 * K * np.pi)
    mask_neg = (x < 0.0)
    mask_seg1 = th.logical_and(rx >= 0.0, rx < np.pi/2)
    mask_seg23 = th.logical_and(rx >= np.pi/2, rx < 3*np.pi/2)
    mask_seg4 = th.logical_and(rx >= 3*np.pi/2, rx < 2*np.pi)
    result = (mask_neg * 0.0)
    result = result + (mask_seg1 * (rx * 2/np.pi))
    result = result + (mask_seg23 * (-2 + rx * 2/np.pi))
    result = result + (mask_seg4 * (-4 + rx * 2/np.pi))
    return result

def pslash(x):
    # pslash activation
    with th.no_grad():
        K = (x / (2 * np.pi)).int()
    rx = x - (2 * K * np.pi)
    mask_neg = (x < 0.0)
    mask_seg1 = th.logical_and(rx >= 0.0, rx < np.pi/2)
    mask_seg2 = th.logical_and(rx >= np.pi/2, rx < np.pi)
    mask_seg3 = th.logical_and(rx >= np.pi, rx < 3*np.pi/2)
    mask_seg4 = th.logical_and(rx >= 3*np.pi/2, rx < 2*np.pi)
    result = (mask_neg * 0.0)
    result = result + (mask_seg1 * (rx * 2/np.pi))
    result = result + (mask_seg2 * (-1 + rx * 2/np.pi))
    result = result + (mask_seg3 * (-2 + rx * 2/np.pi))
    result = result + (mask_seg4 * (-3 + rx * 2/np.pi))
    return result

def pslash(x):
    # pslash activation
    with th.no_grad():
        K = (x / (2 * np.pi)).int()
    rx = x - (2 * K * np.pi)
    mask_neg = (x < 0.0)
    mask_seg1 = th.logical_and(rx >= 0.0, rx < np.pi)
    mask_seg2 = th.logical_and(rx >= np.pi, rx < 2*np.pi)
    result = (mask_neg * 0.0)
    result = result + (mask_seg1 * (rx * 1/np.pi))
    result = result + (mask_seg2 * (-1 + rx * 1/np.pi))
    return result

def plume(x):
    # slash activation
    with th.no_grad():
        K = (x / (2 * np.pi)).int()
    rx = x - (2 * K * np.pi)
    mask_neg = (x < 0.0)
    mask_seg1 = th.logical_and(rx >= 0.0, rx < np.pi/2)
    mask_seg2 = th.logical_and(rx >= np.pi/2, rx < np.pi)
    mask_seg3 = th.logical_and(rx >= np.pi, rx < 3*np.pi/2)
    mask_seg4 = th.logical_and(rx >= 3*np.pi/2, rx < 2*np.pi)
    result = (mask_neg * 0.0)
    result = result + (mask_seg1 * (rx * 2/np.pi))
    result = result + (mask_seg2 * (1 - rx * 2/np.pi))
    result = result + (mask_seg3 * (-2 + rx * 2/np.pi))
    result = result + (mask_seg4 * (3 - rx * 2/np.pi))
    return result

def dsin01(x):
    # decay sin
    mask_pos = (x > 0)
    result = mask_pos * th.exp(-0.1 * x) * th.sin(x)
    return result

def dsin02(x):
    # decay sin
    mask_pos = (x > 0)
    result = mask_pos * th.exp(-0.2 * x) * th.sin(x)
    return result

if __name__ == '__main__':
    x = th.linspace(-2*np.pi, 3*2*np.pi, steps=256)
    print(x)
    y = hsin(x)
    print(y)
    plt.plot(x, y)
    plt.show()
    #test_sawsin()
