import os
import gzip
import numpy as np
import torch as th, torch.utils.data
import pickle
from PIL import Image
from torch.utils.data import Dataset
import torchvision as V
try:
    import utils
except ModuleNotFoundError as e:
    from . import utils
from .cifar10 import unpickle


class Cifar100Dataset(Dataset):
    '''
    the cifar 100 dataset
    '''
    def __init__(self, path, kind='trian', transform=None):
        self.path = path
        self.transform = transform
        #
        file_train = os.path.join(path, 'train')
        file_test = os.path.join(path, 'test')
        file_meta = os.path.join(path, 'meta')
        #
        self.meta = unpickle(file_meta)
        if kind == 'train':
            data = unpickle(file_train)
            images = np.array(data['data']).reshape(-1, 3, 32, 32)
            labels = np.array(data['fine_labels'])
        elif kind == 'test':
            data = unpickle(file_test)
            images = np.array(data['data']).reshape(-1, 3, 32, 32)
            labels = np.array(data['fine_labels'])
        else:
            raise ValueError('unknown kind')
        self.images = images.transpose((0,2,3,1))
        self.labels = labels
    def __len__(self):
        return len(self.labels)
    def __getitem__(self, idx):
        image = Image.fromarray(self.images[idx])
        label = self.labels[idx]
        if self.transform is not None:
            image = self.transform(image)
        return image, label



def get_dataset(path: str, kind='train'):
    """
    Load cifar100 data from `path`
    """
    raise NotImplementedError


def get_loader(path: str, batchsize: int, kind='train'):
    """
    Load cifar10 data and turn them into dataloaders
    """
    if kind == 'train':
        #x_train, y_train = get_dataset(path, kind='train')
        #x_train = utils.renorm(th.from_numpy(x_train).float() / 255.)
        #y_train = th.from_numpy(y_train).long().view(-1, 1)
        #data_train = th.utils.data.TensorDataset(x_train, y_train)
        transform = V.transforms.Compose([
            V.transforms.RandomCrop(32, padding=4),
            V.transforms.RandomHorizontalFlip(),
            V.transforms.ToTensor(),
            V.transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225]),
            ])
        data_train = Cifar100Dataset(path, kind='train', transform=transform)
        loader_train = th.utils.data.DataLoader(data_train,
                batch_size=batchsize, shuffle=True, pin_memory=True, num_workers=4)
        return loader_train
    else:
        #x_test, y_test = get_dataset(path, kind='test')
        #x_test = utils.renorm(th.from_numpy(x_test).float() / 255.)
        #y_test = th.from_numpy(y_test).long().view(-1, 1)
        #data_test = th.utils.data.TensorDataset(x_test, y_test)
        transform = V.transforms.Compose([
            V.transforms.ToTensor(),
            V.transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225]),
            ])
        data_test = Cifar100Dataset(path, kind='test', transform=transform)
        loader_test = th.utils.data.DataLoader(data_test,
                batch_size=batchsize, shuffle=False, pin_memory=True, num_workers=4)
        return loader_test
