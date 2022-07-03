import ujson as json
import argparse
import numpy as np
import functools as ft
import rich
console = rich.get_console()

if __name__ == '__main__':
    ag = argparse.ArgumentParser('Print statistics of JSON dataset')
    ag.add_argument('-j', '--json', type=str, required=True)
    ag = ag.parse_args()
    console.print(ag)

    with open(ag.json, 'rt') as f:
        J = json.load(f)
    console.print(f'[bold white on violet]>_< Statistics of {ag.json}')
    console.print(f' > dataset size {len(J)}')
    console.print(f' > sample[0] {J[0]}')
    num_paths_each_svg = np.array([len(x[1:]) for x in J])
    console.print(f' > number of paths per svg',
            'mean', num_paths_each_svg.mean(),
            'max', num_paths_each_svg.max(),
            'min', num_paths_each_svg.min(),
            '; in-total', len(J), 'svgs')
    path_length_each_svg = np.array(ft.reduce(list.__add__,
        [[len(y['data']) for y in x[1:]] for x in J]))
    console.print(f' > path lens',
            'mean', path_length_each_svg.mean(),
            'max', path_length_each_svg.max(),
            'min', path_length_each_svg.min(),
            '; in-total', num_paths_each_svg.sum(), 'paths')

