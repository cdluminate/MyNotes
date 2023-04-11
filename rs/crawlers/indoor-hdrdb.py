#!/usr/bin/env python3
import sys, os, re, csv, urllib, multiprocessing
from bs4 import BeautifulSoup

URL = "http://indoor.hdrdb.com/datapreview.html"
cache = f"{__file__}.cache"
result = f"{__file__}.tsv"
imagesdir = f"{__file__}.imagesdir"

# cache the webpage
if not os.path.exists(cache):
    print('> downloading webpage')
    html = urllib.request.urlopen(URL).read().decode()
    with open(cache, 'wt') as f:
        f.write(html)
else:
    print('> reading webpage cache')
    with open(cache, 'rt') as f:
        html = f.read()

# parse the webpage
print('> parsing html')
soup = BeautifulSoup(html, "lxml")
tds = soup.find_all("td")

# dump the name-url pairs
print('> dumping name-url pairs to: {cache}')
with open(result, 'wt') as f:
    writer = csv.writer(f, delimiter="\t", lineterminator="\n")
    for td in tds:
        imurl = os.path.join(os.path.dirname(URL),
                td.img.get('src'))
        imname = td.h4.string
        #print(imname, imurl, sep='\t')
        writer.writerow([imname, imurl])

# download images in parallel
def downloader(url):
    basename = os.path.basename(url)
    dest = os.path.join(imagesdir, basename)
    if os.path.exists(dest):
        return
    res = urllib.request.urlopen(url)
    if res.status != 200:
        print(f'Failed to download {url} !')
    else:
        with open(dest, 'wb') as imgfile:
            imgfile.write(res.read())
            print(f'200: {url} -> {dest}')

print('> start downloading ...')
if not os.path.exists(imagesdir):
    os.mkdir(imagesdir)
urls = [os.path.join(os.path.dirname(URL), td.img.get('src')) for td in tds]
with multiprocessing.Pool(8) as pool:
    res = list(pool.map(downloader, urls))

print('>_< Done')
