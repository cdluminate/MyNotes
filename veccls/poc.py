import os
import torch as th
import argparse
import rich
console = rich.get_console()

class LeNet(th.nn.Module):
    """
    LeNet convolutional neural network for classification
    """

    def __init__(self):
        '''
        reference: Caffe-LeNet
        '''
        super(LeNet, self).__init__()
        self.conv1 = th.nn.Conv2d(1, 20, 5, stride=1)
        self.conv2 = th.nn.Conv2d(20, 50, 5, stride=1)
        self.fc1 = th.nn.Linear(800, 500)
        self.fc2 = th.nn.Linear(500, 10)

    def forward(self, x, *, l2norm=False):
        # -1, 1, 28, 28
        x = self.conv1(x)
        # -1, 20, 24, 24
        x = th.nn.functional.max_pool2d(x, kernel_size=2, stride=2)
        # -1, 20, 12, 12
        x = self.conv2(x)
        # -1, 50, 8, 8
        x = th.nn.functional.max_pool2d(x, kernel_size=2, stride=2)
        # -1, 50, 4, 4
        x = x.view(-1, 4 * 4 * 50)
        # -1, 800
        x = th.nn.functional.relu(self.fc1(x))
        # -1, 500
        x = self.fc2(x)
        return x

def action_lenet():
    '''
    print lenet statistics
    '''
    model = LeNet()
    state_dict = model.state_dict()
    th.save(state_dict, 'lenet.pt')
    num_params = sum(param.numel() for param in model.parameters()
            if param.requires_grad)
    console.print('LeNet num parameters:', num_params)
    os.system('ls -lh lenet.pt')

if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('action', type=str,
            choices=('lenet',))
    ag = ag.parse_args()
    console.print(ag)

    if ag.action == 'lenet':
        action_lenet()
