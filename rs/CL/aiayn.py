# http://nlp.seas.harvard.edu/2018/04/03/attention.html

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import copy


def attention(Q, K, V, mask=None, dropout=None):
    'Scaled Dot Product Attention'
    d_k = Q.size(-1)
    scores = th.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_full(mask == 0, -1e9)
    p_attn = th.nn.functional.softmax(scores, dim = -1)
    if dropout is not None:
        p_attn = dropout(p_attn)
    return th.matmul(p_attn, V), p_attn


'''
most competitive neural sequence transduction models have an encoder-decoder
structure. here, the encoder maps an input sequence of symbol representations
(x_1, ..., x_n) to a sequence of continuous representations z=(z_1, ..., z_n).
Given z, the decoder then generates an output sequence (y_1, ..., y_m) of
symbols one element at a time. At each step of the model is auto-regressive,
consuming the previously generated symbols as additional input when generating
the next.
'''

class EncoderDecoder(th.nn.Module):
    '''
    A Standard Encoder-Decoder architecture. Base for AIAYN and other models.
    '''
    def __init__(self, enc, dec, srcemb, dstemb, generator):
        super(EncoderDecoder, self).__init__()
        self.enc, self.dec = enc, dec
        self.srcemb, self.dstemb = srcemb, dstemb
        self.generator = generator

    def encode(self, src, srcmask):
        return self.enc(self.srcemb(src), src_mask)

    def decode(self, mem, srcmask, dst, dstmask):
        return self.dec(self.dstemb(dst), mem, srcmask, dstmask)

    def forward(self, src, dst, srcmask, dstmask):
        return self.dec(self.enc(src, srcmask), srcmask, dst, dstmask)


class Generator(th.nn.Module):
    '''
    Standard linear + softmax generation step
    '''
    def __init__(self, d_model, d_vocab):
        super(Generator, self).__init__()
        self.proj = th.nn.Linear(d_model, d_vocab)

    def forward(self, x):
        return th.nn.functional.log_softmax(self.proj(x), dim=-1)


class Encoder(th.nn.Module):
    '''
    Core Encoder is a stack of N layers
    '''
    def __init__(self, layer, N):
        super(Encoder, self).__init__()
        self.layers = th.nn.ModuleList([copy.deepcopy(layer) for _ in range(N)])
        self.norm = LayerNorm(layer.size)

    def forward(self, x, mask):
        for layer in self.layers:
            x = layer(x, mask)
        return self.norm(x)


class LayerNorm(th.nn.Module):
    def __init__(self, features, eps=1e-6):
        super(LayerNorm, self).__init__()
        self.a_2 = th.nn.Parameter(th.ones(features))
        self.b_2 = th.nn.Parameter(th.zeros(features))
        self.eps = eps
    def forward(self, x):
        mean = x.mean(-1, keepdim=True)
        std = x.std(-1, keepdim=True)
        return self.a_2 * (x-mean)/(std+self.eps) + self.b_2


class SublayerConnection(th.nn.Module):
    '''
    Residual connection followed by a layer norm
    '''
    def __init__(self, size, dropout):
        super(SublayerConnection, self).__init__()
        self.norm = LayerNorm(size)
        self.dropout = th.nn.Dropout(dropout)
    def forward(self, x, sublayer):
        return x + self.dropout(sublayer(self.norm(x)))


class EncoderLayer(th.nn.Module):
    '''
    self-attn and feed forward
    '''
    def __init__(self, size, self_attn, feed_forward, dropout):
        super(EncoderLayer, self).__init__()
        self.self_attn = self_attn
        self.feed_forward = feed_forward
        subl = SublayerConnection(size, dropout)
        self.sublayer = th.nn.ModuleList([copy.deepcopy(subl) for _ in range(2)])
        self.size = size

    def forward(self, x, mask):
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, mask))
        return self.sublayer[1](x, self.feed_forward)


class Decoder(th.nn.Module):
    '''
    Generic N layer decoder with masking
    '''
    def __init__(self, layer, N):
        super(Decoder, self).__init__()
        self.layers = th.nn.ModuleList([copy.deepcopy(layers) for _ in range(2)])
        self.norm = LayerNorm(layer.size)
    def forward(self, x, mem, srcmask, dstmask):
        for layer in self.layers():
            x = layer(x, mem, srcmask, dstmask)
        return self.norm(x)


class DecoderLayer(th.nn.Module):
    '''
    self-attn, src-attn and feed-forward
    '''
    def __init__(self, size, self_attn, src_attn, feed_forward, dropout):
        super(DecoderLayer, self).__init__()
        self.size = size
        self.self_attn = self_attn
        self.src_attn = src_attn
        self.feed_forward = feed_forward
        subl = SublayerConnection(size, dropout)
        self.sublayer = th.nn.ModuleList([copy.deepcopy(subl) for _ in range(3)])
    def forward(self, x, mem, srcmask, dstmask):
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, dstmask))
        x = self.sublayer[1](x, lambda x: self.src_attn(x, mem, mem, srcmask))
        return self.sublayer[2](x, self.feed_forward)


def subsequent_mask(size):
    'mask out subsequent positions'
    attn_shape = (1, size, size)
    mask = np.triu(np.ones(attn_shape), k=1).astype('uint8')
    return th.from_numpy(mask) == 0
