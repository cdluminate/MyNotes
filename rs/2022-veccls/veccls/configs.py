import os
from dataclasses import dataclass

@dataclass
class datasets:
    @dataclass
    class mnist:
        root : str = os.path.expanduser('~/.torch/MNIST')
        jsonpath_train : str = 'mnist-train.json'
        jsonpath_test : str= 'mnist-test.json'
    @dataclass
    class fashion:
        root : str = os.path.expanduser('~/.torch/FashionMNIST')
        jsonpath_train = 'fashion-train.json'
        jsonpath_test = 'fashion-test.json'
    @dataclass
    class cifar10:
        root : str = os.path.expanduser('~/.torch/CIFAR10')
        jsonpath_train = 'cifar10-train.json'
        jsonpath_test = 'cifar10-test.json'
    @dataclass
    class cifar100:
        root : str = os.path.expanduser('~/.torch/CIFAR100')
        jsonpath_train = 'cifar100-train.json'
        jsonpath_test = 'cifar100-test.json'
    @dataclass
    class tinyimagenet:
        '''
        download it here:
        http://cs231n.stanford.edu/tiny-imagenet-200.zip
        '''
        root : str = os.path.expanduser('~/.torch/tiny-imagenet-200')
        jsonpath_train = 'tinyimagenet-train.json'
        jsonpath_test = 'tinyimagenet-test.json'
    @dataclass
    class imagenet1k:
        '''
        use kaggle version 2017
        '''
        root : str = os.path.expanduser('~/.torch/ilsvrc2017')
        jsonpath_train = 'imagenet1k-train.jsond'
        jsonpath_test = 'imagenet1k-test.jsond'
