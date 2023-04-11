'''
Paper List Analyzer / Making statistics from paper list.

usage: python3 THIS paperlist.html TYPE

ref: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
ref: https://stackoverflow.com/questions/16867347/step-by-step-debugging-with-ipython
'''
USE_IPYTHON = True
import bs4
import q    # brilliant dev and dbg util!
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
if USE_IPYTHON:
    import IPython

class RawReader(object):
    '''
    RawReader: Raw File -> List of paper titles
    1. http://openaccess.thecvf.com/ICCV2017.py [downloadable]
    2. https://openreview.net/group?id=ICLR.cc/2018/Conference [copy/paste]
    3. http://openaccess.thecvf.com/CVPR2017.py [downloadable]
    4. https://2017.icml.cc/Conferences/2017/Schedule?type=Poster [download]
    5. https://nips.cc/Conferences/2017/Schedule?type=Poster [download]
    6. XXX: ECCV? 2016, somewhat old.
    '''
    @staticmethod
    def reader_iccv(fpath):
        with open(fpath, 'r') as f:
            content = f.read()
        soup = bs4.BeautifulSoup(content, 'html.parser')
        papers = soup.find_all('dt')
        titles = [x.get_text() for x in papers] # List[str]
        return titles
    @staticmethod
    def reader_iclr(fpath):
        with open(fpath, 'r') as f:
            lines = f.readlines()
        lines = [ line for line in lines if len(line.strip())>0 ] # remove empty
        lines = [ line for line in lines if 'ICLR' not in line ] # remove unrelated
        lines = [ line for line in lines if 'Show paper details' not in line ] # remove useless
        lines = [ line for (i, line) in enumerate(lines) if i % 2 == 0 ] # remove author line
        return lines
    @staticmethod
    def reader_icml(fpath):
        with open(fpath, 'r') as f:
            content = f.read()
        soup = bs4.BeautifulSoup(content, 'html.parser')
        papers = soup.find_all('div', attrs={'class': 'maincardBody'})
        titles = [x.get_text() for x in papers]
        return titles

    reader_cvpr = reader_iccv  # cvpr input format is the same to iccv
    reader_nips = reader_icml  # nips input format is the same to icml


if __name__ == '__main__':

    assert(sys.argv[1] and sys.argv[2])
    titles = eval(f'RawReader.reader_{sys.argv[2]}')(sys.argv[1])

    print('* Found {} paper titles. Dumping ...'.format(len(titles)))
    for (i,v) in enumerate(titles, 1):
        print(i, v)

    # single word statistics
    vocab = defaultdict(int)
    for title in titles:
        words = title.strip().lower().split()
        for w in words:
            vocab[w] += 1
    vrank = sorted(vocab.items(), key=lambda x: x[1], reverse=True)
    #print(vrank)

    # word pair statistics
    vocabd = defaultdict(int)
    for title in titles:
        words = title.strip().lower().split()
        for i in range(len(words)-1):
            pair = ' '.join(words[i:i+2])
            vocabd[pair] += 1
    vdrank = sorted(vocabd.items(), key=lambda x: x[1], reverse=True)
    #vdrank = [x for x in vdrank if x[1]>1]
    #print(vdrank)

    # dump some useful info
    print('vocab len', len(vocab.keys()), 'total count', sum(vocab.values()),
            'avg', sum(vocab.values())/len(vocab.keys()))
    print('vocabd len', len(vocab.keys()), 'total count', sum(vocabd.values()),
            'avg', sum(vocabd.values())/len(vocabd.keys()))
    for i in range(len(vrank)):
        if i >= 50: break
        print(i+1, vrank[i])
    for i in range(len(vdrank)):
        if i >= 50: break
        print(i+1, vdrank[i])

    if USE_IPYTHON:
        IPython.embed() # q.d()
