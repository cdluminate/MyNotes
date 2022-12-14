'''
puftm :: datasets
'''
import numpy as np
import torch as th
from torch.utils.data import DataLoader
import torchvision as V
from torchvision import transforms as T
from . import config


def get_dataset_loader(name: str, split: str):
    if name != 'MNIST':
        raise NotImplementedError
    assert split in ('train', 'test')
    transform = T.Compose([
        T.ToTensor(),
        T.Normalize((0.1307,), (0.3081,)),
        ])
    data = V.datasets.MNIST(root=config.datasets.mnist.root,
            train=(split=='train'),
            download=True,
            transform=transform,
            )
    loader = DataLoader(data,
            batch_size=config.datasets.mnist.batch_size,
            shuffle=(True if split=='train' else False),
            num_workers=config.datasets.mnist.num_workers)
    return loader


def test_get_dataset_loader():
    trainl = get_dataset_loader('MNIST', 'train')
    for (i, l) in trainl:
        assert isinstance(i, th.Tensor)
        assert isinstance(l, th.Tensor)
        break
    testl = get_dataset_loader('MNIST', 'test')
    for (i, l) in testl:
        assert isinstance(i, th.Tensor)
        assert isinstance(l, th.Tensor)
        break
