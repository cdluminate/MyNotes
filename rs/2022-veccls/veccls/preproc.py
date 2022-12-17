try:
    import ujson as json
except ModuleNotFoundError:
    import json
import torch as th
import torchvision as V
from . import configs

if __name__ == '__main__':
    print(f'{__file__}')
