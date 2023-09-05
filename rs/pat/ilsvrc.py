'''
Copyright (C) 2023, Mo Zhou <cdluminate@gmail.com>
pytorch ImageNet dataloader variant for the kaggle data
https://www.kaggle.com/c/imagenet-object-localization-challenge/data
also refer https://github.com/pytorch/examples/blob/main/imagenet/main.py

The root directory is named ILSVRC, which contains the following files:
Annotations/  ImageSets/                 LOC_synset_mapping.txt  LOC_val_solution.csv
Data/         LOC_sample_submission.csv  LOC_train_solution.csv
You may need to move some files around and reorganize a little bit.
'''
import os
import sys
import re
import torch as th
from torch.utils.data import Dataset
import torchvision as V
import numpy as np
from PIL import Image
import rich
from rich.progress import track
c = rich.get_console()

NORMALIZE = V.transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                   std=[0.229, 0.224, 0.225])

TRANS_train = V.transforms.Compose([
    V.transforms.RandomResizedCrop(224),
    V.transforms.RandomHorizontalFlip(),
    V.transforms.ToTensor(),
#    NORMALIZE,
])

TRANS_val = V.transforms.Compose([
    V.transforms.Resize(256),
    V.transforms.CenterCrop(224),
    V.transforms.ToTensor(),
#    NORMALIZE,
])


class ILSVRC(Dataset):
    def load_map_wnid2clsid(self):
        fpath = os.path.join(self.root, 'LOC_synset_mapping.txt')
        if not os.path.exists(fpath):
            raise Exception(f'cannot find {fpath}')
        with open(fpath, 'rt') as f:
            lines = f.readlines()
        lines = [x.strip().split()[0] for x in lines]
        d = {str(wnid): int(i) for (i, wnid) in enumerate(lines)}
        self.wnid2cls = d
        #print(f'ILSVRC] built wnid to classid mapping of size {len(d)}')
        assert(len(d) == 1000)

    def load_train_list(self):
        fpath = os.path.join(self.root, 'ImageSets/CLS-LOC/train_cls.txt')
        if not os.path.exists(fpath):
            raise Exception(f'cannot find {fpath}')
        with open(fpath, 'rt') as f:
            lines = [x.strip().split()[0] for x in f.readlines()]
        lines = [(os.path.join(self.root, 'Data/CLS-LOC/train', x),
                  os.path.dirname(x)) for x in lines]
        lines = [(x[0] + '.JPEG', x[1]) for x in lines]
        # print(lines[-10:])
        print(f'ILSVRC2017] training data set size is {len(lines)}')
        self.imagetuples = lines

    def load_val_list(self):
        fpath = os.path.join(self.root, 'ImageSets/CLS-LOC/val.txt')
        if not os.path.exists(fpath):
            raise Exception(f'cannot find {fpath}')
        with open(fpath, 'rt') as f:
            lines = [x.strip().split()[0] for x in f.readlines()]
        tuples = []
        for l in track(lines, description='ILSVRC2017] reading scattered xml files for validation set'):
            fpath = os.path.join(self.root, 'Data/CLS-LOC/val', l) + '.JPEG'
            xmlpath = os.path.join(self.root, 'Annotations/CLS-LOC/val/',
                                   l) + '.xml'
            with open(xmlpath, 'rt') as f:
                wnid = re.findall('<name>(n\d+)</name>', f.read())[0]
            tuples.append((fpath, wnid))
        # print(tuples[-10:])
        print(f'ILSVRC] val set size {len(tuples)}')
        self.imagetuples = tuples

    def __init__(self, root, split):
        self.root = root
        self.split = split
        self.load_map_wnid2clsid()
        if split == 'train':
            self.transform = TRANS_train
            self.load_train_list()
        elif split == 'val':
            self.transform = TRANS_val
            self.load_val_list()
        else:
            raise ValueError(split)

    def __len__(self):
        return len(self.imagetuples)

    def __getitem__(self, index):
        fpath, wnid = self.imagetuples[index]
        image = Image.open(fpath).convert('RGB')
        label = self.wnid2cls[wnid]
        if self.transform is not None:
            image = self.transform(image)
        return image, label


if __name__ == '__main__':
    root = sys.argv[1]
    trainset = ILSVRC(root, 'train')
    valset = ILSVRC(root, 'val')

    for (i, (im, lb)) in track(enumerate(trainset), total=len(trainset)):
        if i > 100 or len(trainset) - i < 100:
            break
        print(i, im.shape, lb)

    for (i, (im, lb)) in track(enumerate(valset), total=len(valset)):
        if i > 100:
            break
        print(i, im.shape, lb)
