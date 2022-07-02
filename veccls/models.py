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
    def forward(self, input, transcolor=None):
        '''
        input should be pack_padded_sequence result.
        see torch.nn.utils.rnn.pack_padded_sequence
        '''
        B = input[1][0]  # batch size
        if transcolor is None:
            h0 = th.zeros(1, B, self.hidden_size).to(input[0].device)
            h0 = h0.expand(self.num_layers, B, self.hidden_size).contiguous()
        else:
            h0 = self.tc(transcolor).unsqueeze(0)
            h0 = h0.expand(self.num_layers, B, self.hidden_size).contiguous()
        if self.rnn_type in ('rnn', 'gru'):
            output, hn = self.rnn(input, h0)
        else:
            output, (hn, cn) = self.rnn(input, h0)
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
