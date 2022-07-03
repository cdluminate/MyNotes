import os
import argparse
import torch as th
import torch.nn.functional as F
from . import mnist_dataset
from torch.nn.utils.rnn import pad_sequence, pack_sequence, pack_padded_sequence
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
            self.rnn = th.nn.GRU(hidden_size, hidden_size, num_layers)
        elif rnn_type == 'rnn':
            self.rnn = th.nn.RNN(hidden_size, hidden_size, num_layers)
        elif rnn_type == 'lstm':
            self.rnn = th.nn.LSTM(hidden_size, hidden_size, num_layers)
        self.tc = th.nn.Sequential(
                th.nn.Linear(5, hidden_size),
                th.nn.ReLU(),
                th.nn.Linear(hidden_size, hidden_size),
                th.nn.ReLU(),
                th.nn.Linear(hidden_size, hidden_size),
                th.nn.ReLU(),
                )
        self.fc = th.nn.Linear(hidden_size, num_classes)
        self.encoder = th.nn.Linear(input_size, hidden_size)
        self.num_params = sum(param.numel() for param in self.parameters()
                if param.requires_grad)
    def forward(self, x, y, trco, lens, packlens, *, device: str = 'cpu'):
        '''
        input should be pad_sequence result. we pack it by ourselves
        see torch.nn.utils.rnn.pack_padded_sequence
        '''
        B = int(x.shape[1])  # batch size. x is already padded sequence
        x = x.to(device)
        x = self.encoder(x)
        pack = pack_padded_sequence(x, lens)
        pack = pack.to(device)
        y = y.to(device)
        h0 = self.tc(trco.to(device)).unsqueeze(0)
        h0 = h0.expand(self.num_layers, B, self.hidden_size).contiguous()
        if self.rnn_type in ('rnn', 'gru'):
            output, hn = self.rnn(pack, h0)
        else:
            output, (hn, cn) = self.rnn(pack, (h0, h0))
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
        if rnn_type == 'hgru':
            self.pathrnn = th.nn.GRU(hidden_size, hidden_size, num_layers)
            self.svgrnn = th.nn.GRU(hidden_size, hidden_size, num_layers)
        elif rnn_type == 'hrnn':
            self.pathrnn = th.nn.RNN(hidden_size, hidden_size, num_layers)
            self.svgrnn = th.nn.RNN(hidden_size, hidden_size, num_layers)
        elif rnn_type == 'hlstm':
            self.pathrnn = th.nn.LSTM(hidden_size, hidden_size, num_layers)
            self.svgrnn = th.nn.LSTM(hidden_size, hidden_size, num_layers)
        self.pathtc = th.nn.Sequential(
                th.nn.Linear(5, hidden_size),
                th.nn.ReLU(),
                th.nn.Linear(hidden_size, hidden_size),
                th.nn.ReLU(),
                th.nn.Linear(hidden_size, hidden_size),
                th.nn.ReLU(),
                )
        self.svgfc = th.nn.Linear(hidden_size, num_classes)
        self.encoder = th.nn.Linear(input_size, hidden_size) # MLP here harmful
        self.num_params = sum(param.numel() for param in self.parameters()
                if param.requires_grad)
    def forward(self, x, y, trco, lens, packlens, *, device: str='cpu'):
        '''
        x should be padded sequence
        '''
        B = int(x.shape[1]) # batch size
        x = x.to(device)
        x = self.encoder(x)
        pack = pack_padded_sequence(x, lens, enforce_sorted=False)
        pack = pack.to(device)
        y = y.to(device)
        # [hierarchy 1]: per-path representations
        h0 = self.pathtc(trco.to(device)).unsqueeze(0)
        h0 = h0.expand(self.num_layers, B, self.hidden_size).contiguous()
        if self.rnn_type in ('hrnn', 'hgru'):
            output, hn = self.pathrnn(pack, h0)
        else:
            output, (hn, cn) = self.pathrnn(pack, (h0, h0))
        #print('debug:', hn.shape)
        if self.num_layers == 1:
            h = hn.squeeze(0)
        else:
            h = hn[-1, ...]
        # [hierarchi 2]: aggregate path representations into svg repres
        #print(z.packlens)
        starts = packlens.cumsum(dim=0) - packlens
        ends = packlens.cumsum(dim=0)
        #print('path h.shape', h.shape)
        pathr = [h[starts[i]:ends[i]] for i in range(len(ends))]
        #print('pathr shape', len(pathr), [x.shape for x in pathr])
        #pathr = pad_sequence(pathr)
        #print(pathr.shape)
        #packsvg = pack_padded_sequence(pathr, z.packlens, enforce_sorted=False)
        packsvg = pack_sequence(pathr, enforce_sorted=False)
        #print(packsvg)
        packsvg = packsvg.to(device)
        if self.rnn_type in ('hrnn', 'hgru'):
            sout, shn = self.svgrnn(packsvg)
        else:
            sout, (shn, scn) = self.svgrnn(packsvg)
        if self.num_layers == 1:
            hsvg = shn.squeeze(0)
        else:
            hsvg = shn[-1, ...]
        #print(hsvg.shape)
        # hsvg size: (batch_size, num_hidden)
        logits = self.svgfc(hsvg)
        return logits
