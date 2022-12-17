Unsupervised Learning of Sentence Embeddings using Compositional n-Gram Features

Abs
---
The recent tremendous success of unsupervised word embeddings in a multitude of
applications raises the obvious question if similar methods could be derived to
improve embeddings (i.e. semantic representations) of word sequences as well.

This paper presents a simple but efficient unsupervised objective to train
distributed representation of sentences.

Introduction
------------

Within only a few years from their invention, such word representations --
which are based on a simple matrix factorization model as we formalize below --
are now routinely trained on very large amounts of raw text data, and have
become ubiquitous building blocks of a majority of current state-of-the-art NLP
applications.

Surprisingly, for constructing sentence embeddings, naively using averaged word
vectors was recently shown to outperform LSTMs from plain averaging, and for
weighted averaging.

Our model can be seen as an extension of the CBoW training objective to train
sentence instead of word embeddings.

sent2vec is a simple unsupervised model allowing to compoase sentence
embeddings using the word vectors along with n-gram embeddings, simultaneously
training composition and the embedding vectors themselves.

model
------

Conceptually, the model can be interpreted as a natural exetension of the
word-contexts from C-BOW to a larger sentecne context, with the sentence workds
being specifically optimized towards additive combination over the sentence, by
means of the unsupervised objective function.
