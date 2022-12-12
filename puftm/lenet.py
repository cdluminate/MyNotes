'''
puftm :: LeNet Module
'''
import numpy as np
import torch as th
import torch.nn.functional as F


class LeNet(th.nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = th.nn.Conv2d(1, 6, 5, padding=2)
        self.conv2 = th.nn.Conv2d(6, 16, 5)
        self.fc1   = th.nn.Linear(16*5*5, 120)
        self.fc2   = th.nn.Linear(120, 84)
        self.fc3   = th.nn.Linear(84, 10)

    def num_flat_features(self, x):
        return np.prod(x.shape[1:])

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2, 2))
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def test_lenet():
    model = LeNet()
    image = th.rand(10, 1, 28, 28)
    output = model(image)
    assert output.shape[0] == 10
