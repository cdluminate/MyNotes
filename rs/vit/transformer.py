'''
https://lightning.ai/docs/pytorch/stable/notebooks/course_UvA-DL/05-transformers-and-MH-attention.html
'''
import torch as th
import torch.nn.functional as F
import math
import pytest


def scaled_dot_product(q, k, v, mask=None):
    d_k = q.size()[-1]
    attn_logits = th.matmul(q, k.transpose(-2, -1))
    attn_logits = attn_logits / math.sqrt(d_k)
    if mask is not None:
        attn_logits = attn_logits.masked_fill(mask == 0, -9e15)
    attention = F.softmax(attn_logits, dim=-1)
    values = th.matmul(attention, v)
    return values, attention


def test_scaled_dot_product():
    batch, seq_len, d_k = 10, 64, 128
    q = th.randn(seq_len, d_k)
    k = th.randn(seq_len, d_k)
    v = th.randn(seq_len, d_k)
    print('test -- 1')
    print('q,k,v shape', q.shape)
    values, attention = scaled_dot_product(q, k, v)
    print('values shape', values.shape)
    print('attention shape', attention.shape)
    #
    print('test -- 2')
    q = th.randn(batch, seq_len, d_k)
    k = th.randn(batch, seq_len, d_k)
    v = th.randn(batch, seq_len, d_k)
    print('q,k,v shape', q.shape)
    values, attention = scaled_dot_product(q, k, v)
    print('values shape', values.shape)
    print('attention shape', attention.shape)


class MultiheadAttention(th.nn.Module):
    def __init__(self, input_dim, embed_dim, num_heads):
        super().__init__()
        assert embed_dim % num_heads == 0
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.qkv_proj = th.nn.Linear(input_dim, 3 * embed_dim)
        self.o_proj = th.nn.Linear(embed_dim, embed_dim)
        self._reset_parameters()
    def _reset_parameters(self):
        th.nn.init.xavier_uniform_(self.qkv_proj.weight)
        self.qkv_proj.bias.data.fill_(0.)
        th.nn.init.xavier_uniform_(self.o_proj.weight)
        self.o_proj.bias.data.fill_(0.)
    def forward(self, x, mask=None, return_attention=False):
        batch_size, seq_len, embed_dim = x.size()
        qkv = self.qkv_proj(x)
        # separate q, k, v
        qkv = qkv.reshape(batch_size, seq_len, self.num_heads, 3*self.head_dim)
        qkv = qkv.permute(0, 2, 1, 3) # [batch, head, seq_len, 3*head_dim]
        q, k, v = qkv.chunk(3, dim=-1)
        # value
        values, attention = scaled_dot_product(q, k, v, mask=mask)
        values = values.permute(0, 2, 1, 3) # [batch, seq_len, head, 3*head_dim]
        values = values.reshape(batch_size, seq_len, embed_dim)
        o = self.o_proj(values)
        return (o, attention) if return_attention else o


def test_multihead_attention():
    batch, seq_len, d_k = 10, 64, 128
    x = th.randn(batch, seq_len, d_k)
    mha = MultiheadAttention(d_k, d_k, 8)
    print('src shape', x.shape)
    o = mha(x)
    print('out shape', o.shape)


class EncoderLayer(th.nn.Module):
    def __init__(self, input_dim, num_heads, dim_feedforward, dropout=0.0):
        super().__init__()
        self.self_attn = MultiheadAttention(input_dim, input_dim, num_heads)
        self.ffn = th.nn.Sequential(
            th.nn.Linear(input_dim, dim_feedforward),
            th.nn.Dropout(dropout),
            th.nn.ReLU(inplace=True),
            th.nn.Linear(dim_feedforward, input_dim),
            )
        self.norm1 = th.nn.LayerNorm(input_dim)
        self.norm2 = th.nn.LayerNorm(input_dim)
        self.dropout = th.nn.Dropout(dropout)
    def forward(self, x, mask=None):
        # attention part
        attn_out = self.self_attn(x, mask=mask)
        x = x + self.dropout(attn_out)
        x = self.norm1(x)
        # ffn part
        ffn_out = self.ffn(x)
        x = x + self.dropout(ffn_out)
        x = self.norm2(x)
        return x


def test_encoder_layer():
    batch, seq_len, d_k = 10, 64, 128
    src = th.randn(batch, seq_len, d_k)
    enc = EncoderLayer(d_k, 8, 2*d_k, 0.1)
    print('src shape', src.shape)
    mem = enc(src)
    print('mem shape', mem.shape)


class Encoder(th.nn.Module):
    def __init__(self, num_layers, **block_args):
        super().__init__()
        self.layers = th.nn.ModuleList([
            EncoderLayer(**block_args) for _ in range(num_layers)
            ])
    def forward(self, x, mask=None):
        for layer in self.layers:
            x = layer(x, mask=mask)
        return x
    def get_attention_maps(self, x, mask=None):
        attn_maps = []
        for layer in self.layers:
            _, attn = layer.self_attn(x, mask, return_attention=True)
            attn_maps.append(attn)
            x = layer(x)
        return th.stack(attn_maps)


def test_encoder():
    batch, seq_len, d_k = 10, 64, 128
    src = th.randn(batch, seq_len, d_k)
    enc = Encoder(6, input_dim=d_k, num_heads=8, dim_feedforward=2*d_k, dropout=0.1)
    print('src shape', src.shape)
    mem = enc(src)
    print('mem shape', mem.shape)
    attn = enc.get_attention_maps(src)
    print('attn', attn.shape)


class PosEmb(th.nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = th.zeros(max_len, d_model)
        position = th.arange(0, max_len, dtype=th.float).unsqueeze(1)
        div_term = th.exp(th.arange(0, d_model, 2).float() \
            * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = th.sin(position * div_term)
        pe[:, 1::2] = th.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe, persistent=False)
    def forward(self, x):
        x =  x + self.pe[:, :x.size(1)]
        return x


def test_posemb():
    batch, seq_len, d_k = 10, 64, 128
    src = th.randn(batch, seq_len, d_k)
    pe = PosEmb(d_k)
    print('src shape', src.shape)
    src = pe(src)
    print('src+pe shape', src.shape)
