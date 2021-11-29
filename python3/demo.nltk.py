#!/usr/bin/python3
'''
NLTK demo
https://www.nltk.org/
http://www.nltk.org/book (CC-3.0)
http://www.nltk.org/howto/
'''

import nltk
from pprint import pprint
import IPython

#nltk.download()

sentence = '''
Python, the high-level, interactive object oriented language,
includes an extensive class library with lots of goodies for
network programming, system administration, sounds and graphics.
'''

tokens = nltk.word_tokenize(sentence)
pprint(tokens)

tagged = nltk.pos_tag(tokens)
pprint(tagged)

entities = nltk.chunk.ne_chunk(tagged)
pprint(entities)
#entities.draw()

tree = nltk.tree.Tree.fromstring('(S (NP I) (VP (V enjoyed) (NP my cookie)))')
tree.pretty_print(unicodelines=True)

grammar = nltk.grammar.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> 'the' N | N PP | 'the' N PP
VP -> V NP | V PP | V NP PP
N -> 'cat'
N -> 'dog'
N -> 'rug'
V -> 'chased'
V -> 'sat'
P -> 'in'
P -> 'on'
""")

from nltk.parse import RecursiveDescentParser
rd = RecursiveDescentParser(grammar)
tree = rd.parse('the cat chased the dog on the rug'.split())
for x in tree:
    x.pretty_print(unicodelines=True)

from nltk.corpus import treebank
t = treebank.parsed_sents('wsj_0001.mrg')[0]
#t.draw()


###############################################################################

from nltk.book import *
pprint(text1.concordance('monstrous')) # search word
pprint(text1.similar('monstrous'))
pprint(text1.common_contexts(['monstrous', 'gamesome']))
text4.dispersion_plot(['freedom', 'America'])
pprint(text1.count('monstrous'))
pprint(text1.collocations())

fdist1 = FreqDist(text1)
pprint(fdist1)
fdist1.plot(10) # draw top 10
fdist1.tabulate(15) # make table for top 15
fdist1.hapaxes() # low freq list
pprint(fdist1.max()) # highest freq

nltk.edit_distance("humpty", "dumpty")
