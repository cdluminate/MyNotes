'''
puftm :: datasets
'''
import numpy as np
import torch as th
from torch.utils.data import DataLoader
import torchvision as V
from torchvision import transforms as T


def get_dataset_loader(name: str, split: str):
    if name != 'MNIST':
        raise NotImplementedError
    assert split in ('train', 'test')
    transform = T.Compose([
        T.ToTensor(),
        T.Normalize((0.1307,), (0.3081,)),
        ])
    data = V.datasets.MNIST(root='.',
            train=(split=='train'),
            download=True,
            transform=transform,
            )
    loader = DataLoader(data,
            batch_size=100,
            shuffle=(True if split=='train' else False),
            num_workers=0)
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
