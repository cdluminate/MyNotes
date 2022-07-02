import os
import torch as th
import ujson as json
import torch as th
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence
from . import configs


class MNISTDataset(Dataset):
    '''
    JSON based MNIST dataset.
    SVG paths. no raster graphics this time!
    longest means only return one longest path in image
    '''
    def __init__(self, split:str, longest:bool=False):
        assert(split in ('train', 'test'))
        self.split = split
        jsonpath = getattr(configs.datasets.mnist, f'jsonpath_{split}')
        with open(jsonpath, 'rt') as f:
            j = json.load(f)
        self.j = j
        self.longest = longest
    def __len__(self):
        return len(self.j)
    def __getitem__(self, idx):
        width = int(self.j[idx][0]['width'])
        height = int(self.j[idx][0]['height'])
        label = int(self.j[idx][0]['label'])
        paths = sorted(self.j[idx][1:],
                       key=lambda i: len(i['data']),
                       reverse=True)
        if self.longest:
            path = th.tensor(paths[0]['data']).float()  # (seq len, 2)
            path[:,0] /= float(width)
            path[:,1] /= float(height)
            return path, label
        else:
            raise NotImplementedError

def longest_sequence_collate(batch):
    paths, labels = zip(*batch)
    pack = sorted(zip(paths, labels),
            key=lambda i: len(i[0]),
            reverse=True)
    paths, labels = zip(*pack)
    lens = th.tensor([x.shape[0] for x in paths])
    paths = pad_sequence(paths)
    labels = th.tensor(labels)
    return paths, labels, lens

def get_mnist_loader(split: str, batch_size: int, longest: bool):
    assert(split in ('train', 'test'))
    data = MNISTDataset(split=split, longest=longest)
    if longest:
        collate_fn = longest_sequence_collate
    else:
        raise NotImplementedError
    loader = DataLoader(data, batch_size=batch_size,
            shuffle=True if split == 'train' else False,
            num_workers=4, collate_fn=collate_fn)
    return loader

if __name__ == '__main__':
    import rich
    console = rich.get_console()

    console.print('>_< testing mnist dataset: train')
    datatrn = MNISTDataset(split='train', longest=True)
    console.print('trn size', len(datatrn))
    console.print('trn[0]', datatrn[0])

    console.print('>_< testing mnist dataset: test')
    datatst = MNISTDataset(split='test', longest=True)
    console.print('tst size', len(datatst))
    console.print('tst[0]', datatst[0])

    console.print('>_< testing mnist loader: train')
    loadertrn = get_mnist_loader('train', 5, longest=True)
    for (x, y, z) in loadertrn:
        print(x.shape, y.shape, z.shape)
        print('labels', y)
        print('lens', z)
        break
