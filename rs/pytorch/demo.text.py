'''
https://github.com/spro/practical-pytorch/blob/master/glove-word-vectors/glove-word-vectors.ipynb
'''
import torch as th
import torchtext
from pprint import pprint

def w2v(vocab, w):
    return vocab.vectors[vocab.stoi[w]]

def closet(vocab, w, k=10):
    dists = [(x, th.dist(w2v(vocab, w), w2v(vocab, x))) for x in vocab.itos]
    return sorted(dists, key=lambda t: t[1])[:k]

def analogy(vocab, w1, w2, w3, k=10):
    print(w1, '-', w2, '+', '?', '=', w3)
    dists = [(x, th.dist(w2v(vocab, w2) - w2v(vocab, w1) + w2v(vocab, w3), w2v(vocab, x))) for x in vocab.itos]
    dists = sorted(dists, key=lambda t: t[1])
    return [t for t in dists if t[0] not in (w1, w2, w3)][:k]

if __name__ == '__main__':

    print('> loading glove')
    glove = torchtext.vocab.GloVe(name='6B', dim=100)
    print(f' - loaded {len(glove.itos)} words')

    pprint(closet(glove, 'google'))
    pprint(analogy(glove, 'king', 'man', 'queen'))
    pprint(analogy(glove, 'man', 'actor', 'woman'))
    pprint(analogy(glove, 'man', 'actor', 'woman'))
    pprint(analogy(glove, 'cat', 'kitten', 'dog'))
    pprint(analogy(glove, 'dog', 'puppy', 'cat'))
    pprint(analogy(glove, 'russia', 'moscow', 'france'))
    pprint(analogy(glove, 'obama', 'president', 'trump'))
    pprint(analogy(glove, 'rich', 'mansion', 'poor'))
    pprint(analogy(glove, 'elvis', 'rock', 'eminem'))
    pprint(analogy(glove, 'paper', 'newspaper', 'screen'))
    pprint(analogy(glove, 'monet', 'paint', 'michelangelo'))
    pprint(analogy(glove, 'beer', 'barley', 'wine'))
    pprint(analogy(glove, 'earth', 'moon', 'sun')) # Interesting failure mode
    pprint(analogy(glove, 'house', 'roof', 'castle'))
    pprint(analogy(glove, 'building', 'architect', 'software'))
    pprint(analogy(glove, 'boston', 'bruins', 'phoenix'))
    pprint(analogy(glove, 'good', 'heaven', 'bad'))
    pprint(analogy(glove, 'jordan', 'basketball', 'woods'))
