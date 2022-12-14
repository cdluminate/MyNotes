'''
puftm :: static configurations
'''
import os
from dataclasses import dataclass


@dataclass
class datasets:
    @dataclass
    class mnist:
        root : str = os.path.expanduser('~/.torch/MNIST')
        batch_size : int = 100
        num_workers : int = 0


@dataclass
class engine:
    report_every: int = 1
