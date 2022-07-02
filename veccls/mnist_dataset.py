import os
import torch as th
import ujson as json
from easydict import EasyDict
import functools as ft
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
    def __init__(self, split:str, longest:bool=False, *, mnist='mnist'):
        assert(split in ('train', 'test'))
        self.split = split
        jsonpath = getattr(getattr(configs.datasets, mnist), f'jsonpath_{split}')
        with open(jsonpath, 'rt') as f:
            j = json.load(f)
        self.j = j
        self.longest = longest
        self._mnist = mnist
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
            color = paths[0]['fill'].lstrip('#')
            color = list(int(color[i:i+2], 16)/255. for i in (0, 2, 4))
            translate = paths[0]['trans']
            translate[0] /= float(width)
            translate[1] /= float(height)
            transcolor = translate + color
            return path, label, transcolor
        else:
            path = []
            tc = []
            for p in paths:
                data = th.tensor(p['data']).float() # (seq len, 2)
                data[:,0] /= float(width)
                data[:,1] /= float(height)
                path.append(data)
                c = p['fill'].lstrip('#')
                c = list(int(c[i:i+2], 16)/255. for i in (0, 2, 4))
                translate = p['trans']
                translate[0] /= float(width)
                translate[1] /= float(height)
                transcolor = translate + c
                tc.append(transcolor)
            packlen = len(path)
            #path = pad_sequence(path)
            return path, label, tc, packlen

def longest_sequence_collate(batch):
    paths, labels, transcolors = zip(*batch)
    pack = sorted(zip(paths, labels, transcolors),
            key=lambda i: len(i[0]),
            reverse=True)
    paths, labels, transcolors = zip(*pack)
    lens = th.tensor([x.shape[0] for x in paths])
    paths = pad_sequence(paths)
    labels = th.tensor(labels)
    transcolors = th.tensor(transcolors)
    return paths, labels, EasyDict({'tc': transcolors, 'lens': lens})

def indefinite_sequence_collate(batch):
    paths, labels, transcolors, packlens = zip(*batch)
    # don't sort. adjacent paths for single image
    #pack = sorted(zip(paths, labels, transcolors, packlens),
    #        key=lambda i: len(i[0]),
    #        reverse=True)
    #paths, labels, transcolors, packlens = zip(*pack)
    paths = ft.reduce(list.__add__, paths)
    transcolors = ft.reduce(list.__add__, transcolors)

    pathlens = th.tensor([x.shape[0] for x in paths])
    paths = pad_sequence(paths)
    labels = th.tensor(labels)
    transcolors = th.tensor(transcolors)
    packlens = th.tensor(packlens)
    edict = EasyDict()
    edict.tc = transcolors
    edict.lens = pathlens
    edict.packlens = packlens
    return paths, labels, edict

def get_mnist_loader(split: str, batch_size: int, longest: bool, *, mnist='mnist'):
    assert(split in ('train', 'test'))
    data = MNISTDataset(split=split, longest=longest, mnist=mnist)
    if longest:
        collate_fn = longest_sequence_collate
    else:
        collate_fn = indefinite_sequence_collate
    loader = DataLoader(data, batch_size=batch_size,
            shuffle=True if split == 'train' else False,
            pin_memory=True,
            num_workers=4, collate_fn=collate_fn)
    return loader

if __name__ == '__main__':
    import rich
    console = rich.get_console()

    console.print('>_< testing mnist dataset: train (longest)')
    datatrn = MNISTDataset(split='train', longest=True)
    console.print('trn size', len(datatrn))
    console.print('trn[0]', datatrn[0])

    console.print('>_< testing mnist dataset: test (longest)')
    datatst = MNISTDataset(split='test', longest=True)
    console.print('tst size', len(datatst))
    console.print('tst[0]', datatst[0])

    console.print('>_< testing mnist loader: test (longest)')
    loadertrn = get_mnist_loader('train', 5, longest=True)
    for (x, y, z) in loadertrn:
        print(x.shape, y.shape, z.tc.shape, z.lens.shape)
        print('labels', y)
        print('z.lens', z.lens)
        print('z.tc', z.tc)
        break

    console.print('>_< testing mnist dataset: test (all)')
    datatst = MNISTDataset(split='test', longest=False)
    console.print('tst size', len(datatst))
    console.print('tst[0]', datatst[0])

    console.print('>_< testing mnist loader: train (all)')
    loader = get_mnist_loader('train', 5, longest=False)
    for (x, y, z) in loader:
        print(x.shape, y.shape, z.tc.shape, z.lens.shape, z.packlens.shape)
        print('labels', y)
        print('z.lens', z.lens)
        print('z.tc', z.tc)
        print('z.packlens', z.packlens)
        break
