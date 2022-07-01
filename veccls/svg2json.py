'''
convert svg into sequence of numbers (json)
'''
import xml.etree.ElementTree as ET
import re
import numpy as np
import ujson as json
import argparse
import rich
console = rich.get_console()


def burst_path(path: dict):
    '''
    path is dict {data, fill, trans}
    '''
    results = []
    for token in path['data'].split(' '):
        if re.match(r'M[+-]?\d+,[+-]?\d+', token):
            results.append(list())
            cursor = results[-1]
            x, y = re.match(r'M([+-]?\d+),([+-]?\d+)', token).groups()
            x = int(x)
            y = int(y)
            cursor.append([x,y])
        elif re.match(r'L[+-]?\d+,[+-]?\d+', token):
            x, y = re.match(r'L([+-]?\d+),([+-]?\d+)', token).groups()
            x = int(x)
            y = int(y)
            cursor.append([x,y])
        elif re.match(r'Z', token):
            x, y = cursor[0]
            x = int(x)
            y = int(y)
            cursor.append([x,y])
        elif len(token) == 0:
            continue
        else:
            raise Exception(f'cannot parse path token "{token}"')
    if re.match(r'translate\(\d+,\d+\)', path['trans']):
        x, y = re.match(r'translate\((\d+),(\d+)\)', path['trans']).groups()
        x = int(x)
        y = int(y)
        translate = [x, y]
    else:
        raise Exception(f'cannot parse transform {path["trans"]}')
    return [{'data': result,
             'fill': path['fill'],
             'trans': translate }
             for result in results]

def postprocess(seq: list):
    '''
    parse path data according to svg standard 2.0
    '''
    newseq = []
    newseq.append(seq[0]) # meta data
    for path in seq[1:]:
        newseq = newseq + burst_path(path)
    return newseq

def normalize(seq: list):
    '''
    normalize paths in seq. Align the first svg command as M0,0
    after: postprocess(...)
    '''
    newseq = []
    newseq.append(seq[0]) # meta data
    for path in seq[1:]:
        if path['data'][0] == [0,0]:
            newseq.append(path)
        else:
            xy = np.array(path['data'])
            path['trans'][0] += xy[0,0]
            xy[:,0] -= xy[0,0]
            path['trans'][1] += xy[0,1]
            xy[:,1] -= xy[0,1]
            data = xy.tolist()
            path['data'] = data
            newseq.append(path)
    return newseq

def parsesvg(svg: str, verbose:bool = True) -> list:
    '''
    read and parse svg file, and convert to a list of dicts.
    '''
    tree = ET.parse(svg)
    root = tree.getroot()
    assert(root.tag.endswith('svg'))
    width = int(root.attrib['width'])
    height = int(root.attrib['height'])
    if verbose:
        console.print('>_< root.attrib', root.attrib)
    # the first place as meta data
    seq = [root.attrib,]
    for child in root:
        if not child.tag.endswith('path'):
            raise Exception(f'cannot parse svg content {child}')
        data = child.attrib['d']
        fill = child.attrib['fill']
        trans = child.attrib['transform']
        seq.append({'data': data,
            'fill': fill,
            'trans': trans,})
    console.print('raw sequence', seq)
    seq = postprocess(seq)
    console.print('after processing', seq)
    seq = normalize(seq)
    console.print('after normalize', seq)
    return seq


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('-s', '--svg', type=str, required=True)
    ag.add_argument('-j', '--json', type=str, default=None)
    ag.add_argument('-v', '--verbose', type=bool, default=True)
    ag = ag.parse_args()
    console.print(ag)
    
    parsesvg(ag.svg, ag.verbose)
