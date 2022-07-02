import os
import argparse
import torch as th
import torch.nn.functional as F
from . import mnist_dataset
from torch.nn.utils.rnn import pack_padded_sequence, unpack_sequence
import rich
from rich.progress import track
from . import models
from . import engine
console = rich.get_console()


if __name__ == '__main__':
    ag = argparse.ArgumentParser('''Train an MNIST model, vector graphics!
    (1) Passing in the color and translate as h0 to RNN slightly improves
        performance, from 95.5 to 95.8 (model_type=gru), only using longest
    ''')
    # RNN settings
    ag.add_argument('--model_type', type=str, default='gru',
            choices=('rnn', 'gru', 'lstm',
                'hrnn', 'hgru', 'hlstm',
                ))
    ag.add_argument('--input_size', type=int, default=2)
    ag.add_argument('--hidden_size', type=int, default=64)
    ag.add_argument('--num_layers', type=int, default=3)
    # optimizer and training setting
    ag.add_argument('--lr', type=float, default=1e-3)
    ag.add_argument('--epochs', type=int, default=16)
    ag.add_argument('--lr_drop', type=int, default=12)
    ag.add_argument('--device', type=str, default='cpu'
            if not th.cuda.is_available() else 'cuda')
    # logging
    ag.add_argument('--logdir', type=str, default='train_mnist_')
    ag = ag.parse_args()
    ag.logdir = ag.logdir + ag.model_type
    console.print(ag)

    if not os.path.exists(ag.logdir):
        os.mkdir(ag.logdir)

    console.print('[bold white on violet] >_< start training MnistRNN')

    modelmapping = {
            # only use the longest path. one path per image.
            'rnn': models.LongestPathRNN,
            'gru': models.LongestPathRNN,
            'lstm': models.LongestPathRNN,
            # use all paths. number of paths per image is indefinite.
            'hrnn': models.HierarchicalRNN,
            'hgru': models.HierarchicalRNN,
            'hlstm': models.HierarchicalRNN,
            }
    model = modelmapping[ag.model_type](ag.model_type,
            ag.input_size, ag.hidden_size, ag.num_layers).to(ag.device)
    console.print(model)
    console.print(f'-- Number of parameters:', model.num_params)
    optim = th.optim.Adam(model.parameters(), lr=ag.lr)
    scheduler = th.optim.lr_scheduler.MultiStepLR(optim,
            milestones=[ag.lr_drop], gamma=0.1)
    console.print(f'-- Optimizer:', optim)
    console.print(f'-- Scheduler:', scheduler)

    loadertrn = mnist_dataset.get_mnist_loader(split='train',
            batch_size=128, longest=True)
    loadertst = mnist_dataset.get_mnist_loader(split='test',
            batch_size=100, longest=True)

    # evaluate before train
    engine.evaluate(model, loadertst,
            epoch=-1, device=ag.device, logdir=ag.logdir)
    for epoch in range(ag.epochs):
        console.print(f'>_< training epoch {epoch} ...')

        # train one epoch
        engine.train_one_epoch(model, optim, loadertrn,
                epoch=epoch, device=ag.device, logdir=ag.logdir)

        # evaluate
        engine.evaluate(model, loadertst,
                epoch=epoch, device=ag.device, logdir=ag.logdir)

        # adjust learning rate
        scheduler.step()
