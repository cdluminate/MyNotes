import os
from dataclasses import dataclass

@dataclass
class datasets(object):
    @dataclass
    class mnist(object):
        jsonpath_train = 'mnist-train.json'
        jsonpath_test = 'mnist-test.json'
