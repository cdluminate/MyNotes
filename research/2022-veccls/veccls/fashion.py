import argparse
from . import mnist
import functools as ft
import rich
console = rich.get_console()

fashion_burst = ft.partial(mnist.mnist_burst, mnist='fashion')
fashion_collect = ft.partial(mnist.mnist_collect)

if __name__ == '__main__':
    ag = argparse.ArgumentParser('python3 -m veccls.fashion')
    ag.add_argument('action', choices=('burst', 'collect'))
    ag.add_argument('-d', '--destination', default='.', help='dest directory')
    ag.add_argument('-s', '--split', default='train', choices=('train', 'test'))
    ag = ag.parse_args()
    console.print(ag)

    if ag.action == 'burst':
        fashion_burst(ag.destination, ag.split)
    elif ag.action == 'collect':
        fashion_collect(ag.destination)
