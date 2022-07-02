import os
import argparse
import torch as th
import torch.nn.functional as F
from . import mnist_dataset
from torch.nn.utils.rnn import pack_padded_sequence, unpack_sequence
import rich
from rich.progress import track
console = rich.get_console()

class MnistRNN(th.nn.Module):
    '''
    GRU model for MNIST classification
    '''
    def __init__(self, rnn_type,
            input_size, hidden_size, num_layers,
            num_classes: int = 10):
        super(MnistRNN, self).__init__()
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
        self.fc = th.nn.Linear(hidden_size, num_classes)
        self.num_params = sum(param.numel() for param in self.parameters()
                if param.requires_grad)
    def forward(self, input):
        '''
        input should be pack_padded_sequence result.
        see torch.nn.utils.rnn.pack_padded_sequence
        '''
        if self.rnn_type in ('rnn', 'gru'):
            output, hn = self.rnn(input)
        else:
            output, (hn, cn) = self.rnn(input)
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


def train_one_epoch(model, optim, loader,
        *,
        epoch: int = -1,
        device: str = 'cpu',
        report_every: int = 50,
        log: str = None):
    '''
    train for one epoch, literally
    '''
    if log is not None:
        logfile = open(os.path.join(log, 'train_log.txt'), 'at')
    else:
        logfile = None
    for i, (x, y, z) in enumerate(loader):
        pack = pack_padded_sequence(x, z)
        pack = pack.to(device)
        y = y.to(device)
        logits = model(pack)
        #print(logits.shape, y.shape)
        loss = F.cross_entropy(logits, y, reduction='mean')
        optim.zero_grad()
        loss.backward()
        optim.step()

        if (i)%report_every == 0:
            pred = logits.max(dim=1)[1]
            acc = (pred == y).cpu().float().mean().item() * 100
            console.print(f'Eph[{epoch}] ({i+1}/{len(loader)})',
                    f'loss={loss.item():.3f}',
                    f'accuracy={acc:.2f} (/100)',
                    )
            if logfile is not None:
                logfile.write(f'Eph[{epoch}] ({i+1}/{len(loader)}) ')
                logfile.write(f'loss={loss.item():.3f} ')
                logfile.write(f'accuracy={acc:.2f} (/100)')
                logfile.write('\n')


@th.no_grad()
def evaluate(model, loader,
        *,
        epoch: int = -1,
        device: str = 'cpu',
        log: str = None,
        ):
    '''
    evaluate, literally
    '''
    if log is not None:
        logfile = open(os.path.join(log, 'evaluate_log.txt'), 'at')
    else:
        logfile = None
    losses = []
    preds = []
    ys = []
    for (x, y, z) in track(loader, description=f'Evaluation ...'):
        pack = pack_padded_sequence(x, z)
        pack = pack.to(device)
        y = y.to(device)
        logits = model(pack)
        loss = F.cross_entropy(logits, y, reduction='none')

        losses.append(loss)
        ys.append(y)
        preds.append(logits.max(dim=1)[1])
    losses = th.hstack(losses)
    preds = th.hstack(preds)
    ys = th.hstack(ys)
    #console.print(losses.shape, preds.shape, ys.shape)
    mean_loss = losses.mean()
    acc = (preds == ys).cpu().float().mean().item() * 100
    console.print(f'Eph[{epoch}] Evaluation:',
            f'loss={mean_loss:.2f}',
            f'acc={acc:.2f} (/100)')
    if logfile is not None:
        logfile.write(f'Eph[{epoch}] Evaluation: ')
        logfile.write(f'loss={mean_loss:.2f} ')
        logfile.write(f'acc={acc:.2f} (/100) ')
        logfile.write('\n')

        state_dict = {k: v.cpu() for k, v in model.state_dict()}
        ptpath = os.path.join(log, f'model_eph_{epoch}.pt')
        th.save(state_dict, ptpath)
        console.print(f'Model state dictionary dumped to: {ptpath}')


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
    ag.add_argument('--device', type=str, default='cpu'
            if not th.cuda.is_available() else 'cuda')
    # logging
    ag.add_argument('--log', type=str, default='temp_experiment')
    ag = ag.parse_args()
    console.print(ag)

    if not os.path.exists(ag.log):
        os.mkdir(ag.log)

    console.print('[bold white on violet] >_< start training MnistGRU')

    model = MnistRNN(ag.rnn_type,
            ag.input_size, ag.hidden_size, ag.num_layers).to(ag.device)
    console.print(model)
    console.print(f'-- Number of parameters:', model.num_params)
    optim = th.optim.Adam(model.parameters(), lr=ag.lr)

    loadertrn = mnist_dataset.get_mnist_loader(split='train',
            batch_size=128, longest=True)
    loadertst = mnist_dataset.get_mnist_loader(split='test',
            batch_size=100, longest=True)

    for epoch in range(ag.epochs):
        console.print(f'>_< training epoch {epoch} ...')

        train_one_epoch(model, optim, loadertrn,
                epoch=epoch, device=ag.device, log=ag.log)

        evaluate(model, loadertst,
                epoch=epoch, device=ag.device, log=ag.log)
