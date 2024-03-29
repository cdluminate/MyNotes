import os
import torch as th
import ujson as json
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
            packlen = 1
            return (path, label, transcolor, packlen)
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
            return (path, label, tc, packlen)

def longest_sequence_collate(batch):
    paths, labels, transcolors, packlens = zip(*batch)
    pack = sorted(zip(paths, labels, transcolors, packlens),
            key=lambda i: len(i[0]),
            reverse=True)
    paths, labels, transcolors, packlens = zip(*pack)
    lens = th.tensor([x.shape[0] for x in paths])
    paths = pad_sequence(paths)
    labels = th.tensor(labels)
    transcolors = th.tensor(transcolors)
    packlens = th.tensor(packlens)
    return (paths, labels, transcolors, lens, packlens)

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
    return (paths, labels, transcolors, pathlens, packlens)

def get_mnist_loader(split: str, batch_size: int, longest: bool, *, mnist='mnist'):
    assert(split in ('train', 'test'))
    data = MNISTDataset(split=split, longest=longest, mnist=mnist)
    if longest:
        collate_fn = longest_sequence_collate
    else:
        collate_fn = indefinite_sequence_collate
    shuffle = True if split == 'train' else False
    pin_memory = True if os.getenv('LOCAL_RANK', None) is None else False
    num_workers = 4 if os.getenv('LOCAL_RANK', None) is None else 0
    sampler = None
    if os.getenv('LOCAL_RANK', None) is not None:
        from torch.utils.data.distributed import DistributedSampler
        world_size = th.distributed.get_world_size()
        local_rank = int(os.getenv('LOCAL_RANK'))
        sampler = DistributedSampler(data, num_replicas=world_size,
                rank=local_rank, shuffle=shuffle)
        loader = DataLoader(data, batch_size=batch_size,
                pin_memory=pin_memory,
                num_workers=num_workers, collate_fn=collate_fn,
                sampler=sampler)
    else:
        loader = DataLoader(data, batch_size=batch_size,
                shuffle=shuffle, pin_memory=pin_memory,
                num_workers=num_workers, collate_fn=collate_fn,
                sampler=sampler)
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
    for (x, y, trco, lens, packlens) in loadertrn:
        print(x.shape, y.shape, trco.shape, lens.shape, packlens.shape)
        print('labels', y)
        print('trco', trco)
        print('lens', lens)
        print('packlens', packlens)
        break

    console.print('>_< testing mnist dataset: test (all)')
    datatst = MNISTDataset(split='test', longest=False)
    console.print('tst size', len(datatst))
    console.print('tst[0]', datatst[0])

    console.print('>_< testing mnist loader: train (all)')
    loader = get_mnist_loader('train', 5, longest=False)
    for (x, y, trco, lens, packlens) in loader:
        print(x.shape, y.shape, trco.shape, lens.shape, packlens.shape)
        print('labels', y)
        print('trco', trco)
        print('lens', lens)
        print('packlens', packlens)
        break
