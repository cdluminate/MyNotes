import os
import argparse
import torchvision as V
import matplotlib.pyplot as plt
import ujson as json
import rich
console = rich.get_console()

def mnist_burst(dest: str, split: str):
    '''
    burst mnist dataset into png images
    '''
    assert(split in ('train', 'test'))
    if not os.path.exists(dest):
        os.mkdir(dest)
    data = V.datasets.MNIST(root=os.path.expanduser('~/.torch/MNIST'),
                            train=True if split=='train' else False)
    for i, (x, y) in enumerate(data):
        fpath = os.path.join(dest, '%05d.png'%i)
        x.save(fpath)
        console.print(fpath)
        print(x, y)
    print(len(data))

if __name__ == '__main__':
    ag = argparse.ArgumentParser('python3 -m veccls.mnist')
    ag.add_argument('action', choices=('burst',))
    ag.add_argument('-d', '--destination', default='.', help='dest directory')
    ag.add_argument('-s', '--split', default='train', choices=('train', 'test'))
    ag = ag.parse_args()
    console.print(ag)

    if ag.action == 'burst':
        mnist_burst(ag.destination, ag.split)
