import os
from PIL import Image
import PIL.ImageOps
import argparse
import torchvision as V
import matplotlib.pyplot as plt
import ujson as json
import glob
import re
from . import configs
import rich
from rich.progress import track
console = rich.get_console()

def mnist_burst(dest: str, split: str, *,
        mnist='mnist'):
    '''
    burst mnist dataset into png images

    svg background is white by default in vtracer,
    and hence the polygons draw the background.
    We need to invert the color, so that the paths are drawing
    the foreground object.
    '''
    assert(split in ('train', 'test'))
    assert(mnist in ('mnist', 'fashion'))
    if not os.path.exists(dest):
        os.mkdir(dest)
    if mnist == 'mnist':
        data = V.datasets.MNIST(root=configs.mnist.root,
                            train=True if split=='train' else False,
                            download=True)
    elif mnist == 'fashion':
        data = V.datasets.FashionMNIST(root=configs.fashion.root,
                            train=True if split=='train' else False,
                            download=True)
    for i, (x, y) in enumerate(data):
        fpath = os.path.join(dest, '%05d-%1d.png'%(i, y))
        xinv = PIL.ImageOps.invert(x)
        xinv.save(fpath)
        console.print(fpath)
        print(x, y)
    print(len(data))


def mnist_collect(src: str):
    '''
    collect processed data from
    '''
    dataset = []
    files = glob.glob(os.path.join(src, '*.json'))
    for file in track(files):
        with open(file, 'rt') as f:
            j = json.load(f)
        label = re.match(r'.*/\d+-(\d).json', file).groups()[0]
        j[0]['label'] = int(label)
        dataset.append(j)
    with open(src+'.json', 'wt') as f:
        json.dump(dataset, f)
    console.print('>_< done')


if __name__ == '__main__':
    ag = argparse.ArgumentParser('python3 -m veccls.mnist')
    ag.add_argument('action', choices=('burst', 'collect'))
    ag.add_argument('-d', '--destination', default='.', help='dest directory')
    ag.add_argument('-s', '--split', default='train', choices=('train', 'test'))
    ag = ag.parse_args()
    console.print(ag)

    if ag.action == 'burst':
        mnist_burst(ag.destination, ag.split)
    elif ag.action == 'collect':
        mnist_collect(ag.destination)
