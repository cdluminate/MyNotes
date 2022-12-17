'''
reference:
https://github.com/llSourcell/word_vectors_game_of_thrones-LIVE
'''
import glob, os, re, sys
import argparse
import spacy
import tqdm
from collections import Counter
import gensim.models.word2vec as gensimw2v
import ujson as json


def mainTrain(argv):
    '''
    Train word2vec model
    '''
    ag = argparse.ArgumentParser()
    ag.add_argument('--src', type=str,
            default='word_vectors_game_of_thrones-LIVE/data/*.txt')
    ag.add_argument('--tokcache', type=str, default=f'{__file__}.tokcache')
    ag.add_argument('--save', type=str, default=f'{__file__}.model')
    ag = ag.parse_args(argv)
    print('=> AG:', ag)

    books = list(sorted(glob.glob(ag.src)))
    print('=> Books:', books)

    Lall = []
    for b in books:
        lines = open(b, 'r').readlines()
        print(' ->', len(lines), 'lines in', b)
        Lall.extend(lines)
    print(' ->', len(Lall), 'lines in total')

    print('*> tokenization')
    if os.path.exists(ag.tokcache):
        print(' -> loading tokenization cache from', ag.tokcache)
        ctr, Lall = json.load(open(ag.tokcache, 'r'))
    else:
        ctr = Counter()
        nlp = spacy.load('en_core_web_sm')
        for (i, l) in tqdm.tqdm(enumerate(Lall), total=len(Lall)):
            tok = [x.text for x in nlp(l) if x.is_alpha]
            if len(tok) == 0: continue
            Lall[i] = tok
            ctr.update(tok)
        json.dump([ctr, Lall], open(ag.tokcache, 'w'))

    print('*> word2vec')
    w2v = gensimw2v.Word2Vec(sg=1, seed=1, workers=4, size=300,
            min_count=3, window=7, sample=1e-3)
    w2v.build_vocab(Lall)
    print(' -> training')
    w2v.train(Lall, total_examples=len(Lall), epochs=10)
    w2v.save(ag.save)


def mainVis(argv):
    ag = argparse.ArgumentParser()
    ag.add_argument('--model', type=str, default=f'{__file__}.model')
    ag = ag.parse_args(argv)
    print('=> AG:', ag)

    w2v = gensimw2v.Word2Vec.load(ag.model)
    print(w2v.most_similar("Stark"))
    print(w2v.most_similar("Aerys"))
    print(w2v.most_similar("direwolf"))


if __name__ == '__main__':
    eval(f'main{sys.argv[1]}')(sys.argv[2:])
