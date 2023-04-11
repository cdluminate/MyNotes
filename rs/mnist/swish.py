# https://discuss.pytorch.org/t/implementation-of-swish-a-self-gated-activation-function/8813
# http://pytorch.org/docs/master/notes/extending.html
# http://pytorch.org/tutorials/beginner/examples_autograd/two_layer_net_custom_function.html

import torch as th
import torch.nn.functional as F

def swish(x):
    return x * F.sigmoid(x)

class SwishF(th.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        result = input * input.sigmoid()
        ctx.save_for_backward(result, input)
        return result
    def backward(ctx, grad_output):
        result, input = ctx.saved_variables
        sigmoid_x = input.sigmoid()
        return grad_output * (result + sigmoid_x * (1-result))

swishf = SwishF.apply

class SwishModule(th.nn.Module):
    def forward(self, x):
        #return swish(x)
        return swishf(x)
