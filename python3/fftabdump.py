'''
Dump list of firefox opened tabs.

open `about:profiles` from firefox to see a list of profiles.
'''
import json
import os
import argparse
import re
import rich
import socket
c = rich.get_console()

ag = argparse.ArgumentParser()
ag.add_argument('-p', '--profile', type=str, help='profile name')
ag.add_argument('--save', action='store_true')
ag.add_argument('-d', '--dest', type=str, default='./')
ag = ag.parse_args()

jsonlz4_path = os.path.expanduser(f'~/.mozilla/firefox/{ag.profile}/sessionstore.jsonlz4')
assert(os.path.exists(jsonlz4_path))
json_path = re.sub(r'\.jsonlz4$', '.json', jsonlz4_path)
os.system(f'lz4jsoncat {jsonlz4_path} > {json_path}')
assert(os.path.exists(json_path))
c.print(json_path)

with open(json_path, 'rt') as f:
    js = json.load(f)

tabs = js['windows'][0]['tabs']
ds = []
for tab in tabs:
    title = tab['entries'][-1]['title']
    url = tab['entries'][-1]['url']
    originaluri = tab['entries'][-1]['originalURI']
    d = {'Title': title, 'URL': url, 'OriginalURI': originaluri}
    c.print(d)
    ds.append(d)

if ag.save:
    hostname = socket.gethostname()
    dst = os.path.join(ag.dest, f'fftabdump.{hostname}.json')
    with open(dst, 'w') as f:
        json.dump(ds, f, indent=1)
