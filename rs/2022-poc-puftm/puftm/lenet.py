'''
puftm :: LeNet Module
'''
import numpy as np
import torch as th
import torch.nn.functional as F
import pytest


class LeNet(th.nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = th.nn.Conv2d(1, 6, 5, padding=2)
        self.conv2 = th.nn.Conv2d(6, 16, 5)
        self.flat = th.nn.Flatten()
        self.fc1   = th.nn.Linear(16*5*5, 120)
        self.fc2   = th.nn.Linear(120, 84)
        self.fc3   = th.nn.Linear(84, 10)

    def forward(self, x: th.Tensor):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2, 2))
        x = self.flat(x)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def test_lenet():
    model = LeNet()
    image = th.rand(10, 1, 28, 28)
    output = model(image)
    assert output.shape[0] == 10


@pytest.mark.parametrize(
        'layername', ['conv1', 'conv2', 'fc1', 'fc2', 'fc3'])
def test_featuregetter(layername):
    from torchvision.models._utils import IntermediateLayerGetter
    model = LeNet()
    image = th.rand(3, 1, 28, 28)
    if layername in ('conv1',):
        # it does not work very well with functional modules
        feax = IntermediateLayerGetter(model, {layername: 'feat1'})
        out = feax(image)
        print(out['feat1'].shape)
    else:
        activation = {}
        def get_activation(name):
            def hook(model, input, output):
                activation[name] = output.detach()
            return hook
        getattr(model, layername).register_forward_hook(
                get_activation(layername))
        y = model(image)
        out = activation[layername]
        print(out.shape)
