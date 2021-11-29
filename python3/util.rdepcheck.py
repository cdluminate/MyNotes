#!/usr/bin/python3
from typing import *
import sys
import os
import re
import argparse
import json
from collections import Counter


def parsePackages(lines: List[str]) -> List[List[str]]:
    pkg = dict()
    package, bdep, dep = '', [], []
    for line in lines:
        if re.match('^Package:', line):
            package = re.sub('^Package:\w*(\S*)\w*$', '\\1', line)
        elif re.match('^Build-Depends:', line):
            line = re.sub('^Build-Depends:(.*)$', '\\1', line)
            bdep = [x.split()[0] for x in line.split(',')]
        elif re.match('^Depends:', line):
            line = re.sub('^Depends:(.*)$', '\\1', line)
            dep = [x.split()[0] for x in line.split(',')]
        elif re.match('^\w*$', line):
            pkg[package] = {'bdep': bdep, 'dep': dep}
            package, bdep, dep = '', [], []
        else:
            pass
    return pkg


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('-f', '--file', type=str,
            default='/var/lib/apt/lists/mirrors.ustc.edu.cn_debian_dists_sid_main_binary-amd64_Packages')
    ag = ag.parse_args()

    lines = [line.strip() for line in open(ag.file, 'r').readlines()]
    print(f'Read {len(lines)} lines from {ag.file}')
    pkg = parsePackages(lines)
    #print(json.dumps(pkg, indent=2))

    rdepctr = Counter()
    for name, deps in pkg.items():
        rdepctr.update(deps['bdep'])
        rdepctr.update(deps['dep'])
    for k, v in rdepctr.most_common(100):
        print(k, v)
