import os
from dataclasses import dataclass

@dataclass
class datasets(object):
    @dataclass
    class mnist(object):
        root : str = os.path.expanduser('~/.torch/MNIST')
        jsonpath_train : str = 'mnist-train.json'
        jsonpath_test : str= 'mnist-test.json'
    @dataclass
    class fashion(object):
        root : str = os.path.expanduser('~/.torch/FashionMNIST')
        jsonpath_train = 'fashion-train.json'
        jsonpath_test = 'fashion-test.json'
    @dataclass
    class cifar10(object):
        root : str = os.path.expanduser('~/.torch/CIFAR10')
        jsonpath_train = 'cifar10-train.json'
        jsonpath_test = 'cifar10-test.json'
