import os
import argparse
import torch as th
import rich
console = rich.get_console()

class MnistGRU(th.nn.Module):
    '''
    GRU model for MNIST classification
    '''
    def __init__(self, input_size, hidden_size, num_layers):
        super(MnistGRU, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.gru = th.nn.GRU(input_size, hidden_size, num_layers)
    def forward(self, input, h0):
        output, hn = self.gru(input, h0)
        return output, hn

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size)


def train_one_epoch(model, loader):
    pass

def evaluate(model, loader):
    pass

if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--input_size', type=int, default=2)
    ag.add_argument('--hidden_size', type=int, default=32)
    ag.add_argument('--num_layers', type=int, default=2)
    ag = ag.parse_args()
    console.print(ag)

    console.print('[bold white on violet] >_< start training MnistGRU')

    model = MnistGRU(ag.input_size, ag.hidden_size, ag.num_layers)
    console.print(model)
