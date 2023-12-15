import torch as th
import pytest

def test_conv2d():
    # input
    src = th.randn(1, 3, 32, 32)
    assert src.shape == (1, 3, 32, 32)
    # conv layer
    conv = th.nn.Conv2d(3, 8, kernel_size=(3, 3), stride=1, padding=0)
    assert conv.weight.shape == (8, 3, 3, 3)
    assert conv.bias.shape == (8,)
    # output
    dst = conv(src)
    assert dst.shape == (1, 8, 30, 30)
    # test 2
    conv = th.nn.Conv2d(3, 8, kernel_size=3, stride=2, padding=0)
    assert conv(src).shape == (1, 8, 15, 15)
