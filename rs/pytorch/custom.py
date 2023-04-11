'''
https://pytorch.org/tutorials/advanced/numpy_extensions_tutorial.html
'''
import sys
import torch as th
import numpy as np
import scipy.signal


class BadFFTFunction(th.autograd.Function):
    '''
    Parameter-less example
    '''
    
    def forward(self, input):
        np_input = input.detach().numpy()
        result = abs(np.fft.rfft2(np_input))
        return input.new(result)

    def backward(self, grad_output):
        np_go = grad_output.numpy()
        result = np.fft.irfft2(np_go)
        return grad_output.new(result)


def incorrect_fft(input):
    return BadFFTFunction()(input)


class ScipyConv2dFunction(th.autograd.Function):

    @staticmethod
    def forward(ctx, inp, fil, bias):
        inp, fil, bias = inp.detach(), fil.detach(), bias.detach()
        result = scipy.signal.correlate2d(inp.numpy(), fil.numpy(), mode='valid')
        result += bias.numpy()
        ctx.save_for_backward(inp, fil, bias)
        return th.as_tensor(result, dtype=inp.dtype)

    @staticmethod
    def backward(ctx, grad_output):
        grad_output = grad_output.detach()
        inp, fil, bias = ctx.saved_tensors
        grad_output = grad_output.numpy()
        grad_bias = np.sum(grad_output, keepdims=True)
        grad_input = scipy.signal.convolve2d(grad_output, fil.numpy(), mode='full')
        grad_fil = scipy.signal.correlate2d(inp.numpy(), grad_output, mode='valid')
        return th.from_numpy(grad_input), th.from_numpy(grad_fil).to(th.float), \
                th.from_numpy(grad_bias).to(th.float)


class ScipyConv2d(th.nn.Module):

    def __init__(self, filter_width, filter_height):
        super(ScipyConv2d, self).__init__()
        self.filter = th.nn.Parameter(th.randn(filter_width, filter_height))
        self.bias = th.nn.Parameter(th.randn(1, 1))

    def forward(self, input):
        return ScipyConv2dFunction.apply(input, self.filter, self.bias)


def test_scipy_module():
    mod = ScipyConv2d(3, 3)
    print('filter and bias:', list(mod.parameters()))
    x = th.randn(10, 10, requires_grad=True)
    output = mod(x)
    print('output', output)
    output.backward(th.randn(8, 8))
    print('gradient for the input map', x.grad)


if __name__ == '__main__':
    x = th.randn(8, 8, requires_grad=True)
    result = incorrect_fft(x)
    print(result)
    result.backward(th.randn(result.size()))
    print(x)

    test_scipy_module()
