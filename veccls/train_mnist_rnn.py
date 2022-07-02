import os
import argparse
import torch as th
from . import mnist_dataset
from torch.nn.utils.rnn import pack_padded_sequence
import rich
console = rich.get_console()

class MnistRNN(th.nn.Module):
    '''
    GRU model for MNIST classification
    '''
    def __init__(self, rnn_type, input_size, hidden_size, num_layers):
        super(MnistRNN, self).__init__()
        self.rnn_type = rnn_type
        self.input_size = input_size
        self.hidden_size = hidden_size
        if rnn_type == 'gru':
            self.rnn = th.nn.GRU(input_size, hidden_size, num_layers)
        elif rnn_type == 'rnn':
            self.rnn = th.nn.RNN(input_size, hidden_size, num_layers)
        elif rnn_type == 'lstm':
            self.rnn = th.nn.LSTM(input_size, hidden_size, num_layers)
    def forward(self, input):
        '''
        input should be pack_padded_sequence result.
        see torch.nn.utils.rnn.pack_padded_sequence
        '''
        if self.rnn_type in ('rnn', 'gru'):
            output, hn = self.rnn(input)
        else:
            output, (hn, cn) = self.rnn(input)
        return output, hn


def train_one_epoch(model, loader):
    '''
    train for one epoch, literally
    '''
    for (x, y, z) in loader:
        pack = pack_padded_sequence(x, z)
        output, hn = model(pack)
        print(output.shape, hn.shape)
        break

def evaluate(model, loader):
    pass

if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    # RNN settings
    ag.add_argument('--rnn_type', type=str, default='gru',
            choices=('rnn', 'gru', 'lstm'))
    ag.add_argument('--input_size', type=int, default=2)
    ag.add_argument('--hidden_size', type=int, default=32)
    ag.add_argument('--num_layers', type=int, default=2)
    # optimizer and training setting
    ag.add_argument('--lr', type=float, default=1e-3)
    ag.add_argument('--epochs', type=int, default=10)
    ag = ag.parse_args()
    console.print(ag)

    console.print('[bold white on violet] >_< start training MnistGRU')

    model = MnistRNN(ag.rnn_type,
            ag.input_size, ag.hidden_size, ag.num_layers)
    console.print(model)
    optim = th.optim.Adam(model.parameters(), lr=ag.lr)

    loader = mnist_dataset.get_mnist_loader(split='train',
            batch_size=128, longest=True)

    for epoch in range(ag.epochs):
        console.print(f'>_< training epoch {epoch}')

        train_one_epoch(model, loader)
