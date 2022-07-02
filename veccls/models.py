import os
import argparse
import torch as th
import torch.nn.functional as F
from . import mnist_dataset
from torch.nn.utils.rnn import pack_padded_sequence, unpack_sequence
import rich
from rich.progress import track
console = rich.get_console()

class LongestPathRNN(th.nn.Module):
    '''
    RNN,GRU,LSTM model for image classification
    this class only uses the longest path in svg
    '''
    def __init__(self, rnn_type,
            input_size, hidden_size, num_layers,
            num_classes: int = 10):
        super(LongestPathRNN, self).__init__()
        self.rnn_type = rnn_type
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        if rnn_type == 'gru':
            self.rnn = th.nn.GRU(input_size, hidden_size, num_layers)
        elif rnn_type == 'rnn':
            self.rnn = th.nn.RNN(input_size, hidden_size, num_layers)
        elif rnn_type == 'lstm':
            self.rnn = th.nn.LSTM(input_size, hidden_size, num_layers)
        self.tc = th.nn.Sequential(
                th.nn.Linear(5, hidden_size),
                th.nn.ReLU(),
                )
        self.fc = th.nn.Linear(hidden_size, num_classes)
        self.num_params = sum(param.numel() for param in self.parameters()
                if param.requires_grad)
    def forward(self, x, y, z, *, device: str = 'cpu'):
        '''
        input should be pack_padded_sequence result.
        see torch.nn.utils.rnn.pack_padded_sequence
        '''
        B = int(x.shape[1])  # batch size. x is already padded sequence
        pack = pack_padded_sequence(x, z.lens)
        pack = pack.to(device)
        y = y.to(device)
        if not hasattr(z, 'tc'):
            h0 = th.zeros(1, B, self.hidden_size).to(pack[0].device)
            h0 = h0.expand(self.num_layers, B, self.hidden_size).contiguous()
        else:
            h0 = self.tc(z.tc.to(device)).unsqueeze(0)
            h0 = h0.expand(self.num_layers, B, self.hidden_size).contiguous()
        if self.rnn_type in ('rnn', 'gru'):
            output, hn = self.rnn(pack, h0)
        else:
            output, (hn, cn) = self.rnn(pack, h0)
        #return output, hn
        #unpack = unpack_sequence(output)
        #print([x.shape for x in unpack])
        #print(hn.shape)
        if self.num_layers == 1:
            h = hn.squeeze(0)
        else:
            h = hn[-1, ...]
        # h size: (batch_size, num_hidden)
        logits = self.fc(h)
        return logits

class HierarchicalRNN(th.nn.Module):
    '''
    this class uses all paths within svg
    '''
    def __init__(self, rnn_type,
            input_size, hidden_size, num_layers,
            num_classes: int = 10):
        super(HierarchicalRNN, self).__init__()
        self.rnn_type = rnn_type
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        if rnn_type == 'gru':
            self.pathrnn = th.nn.GRU(input_size, hidden_size, num_layers)
            self.svgrnn = th.nn.GRU(hidden_size, hidden_size, num_layers)
        elif rnn_type == 'rnn':
            self.pathrnn = th.nn.RNN(input_size, hidden_size, num_layers)
            self.svgrnn = th.nn.RNN(hidden_size, hidden_size, num_layers)
        elif rnn_type == 'lstm':
            self.pathrnn = th.nn.LSTM(input_size, hidden_size, num_layers)
            self.svgrnn = th.nn.LSTM(hidden_size, hidden_size, num_layers)
        self.pathtc = th.nn.Sequential(
                th.nn.Linear(5, hidden_size),
                th.nn.ReLU())
        self.svgfc = th.nn.Linear(hidden_size, num_classes)
        self.num_params = sum(param.numel() for param in self.parameters()
                if param.requires_grad)
    def forward(self, x, y, z, *, device: str='cpu'):
        raise NotImplementedError


