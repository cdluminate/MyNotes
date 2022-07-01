'''
convert svg into sequence of numbers (json)
'''
import xml.etree.ElementTree as ET
import ujson as json
import argparse
import rich
console = rich.get_console()

def postprocess(seq: str):
    '''
    parse path data according to svg standard 2.0
    '''
    pass

def parsesvg(svg: str, json: str, verbose:bool = True) -> list:
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


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('-s', '--svg', type=str, required=True)
    ag.add_argument('-j', '--json', type=str, default=None)
    ag.add_argument('-v', '--verbose', type=bool, default=True)
    ag = ag.parse_args()
    console.print(ag)
    
    parsesvg(ag.svg, ag.json, ag.verbose)
