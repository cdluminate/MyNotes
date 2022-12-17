from . import mnist_dataset
import functools as ft

get_fashion_loader = ft.partial(mnist_dataset.get_mnist_loader, mnist='fashion')

if __name__ == '__main__':
    print('we don not have to test this')
