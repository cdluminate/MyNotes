import os
import argparse
from . import svg2json
import numpy as np
import ujson as json
import glob
import rich
from rich.progress import track
console = rich.get_console()

def batch_svg2json(src: str):
    '''
    glob svg files and automatically do the conversion
    '''
    svgs = glob.glob(os.path.join(src, '*.svg'))
    console.print(f'{__name__} >_< found {len(svgs)} svg files.')
    def convert(o):
        if isinstance(o, np.int64):
            return int(o)
        raise TypeError
    for svg in track(svgs):
        jpath = svg.rstrip('.svg')+'.json'
        j = svg2json.parsesvg(svg, False)
        with open(jpath, 'wt') as f:
            json.dump(j, f, default=convert)
        console.print(f'>_< dumped result to {jpath}')

if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('-s', '--source', help='directory containing svgs', required=True)
    ag = ag.parse_args()
    console.print(ag)

    batch_svg2json(ag.source)
