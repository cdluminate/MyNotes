import torch as th
import math
import rich
console = rich.get_console()

class PositionalEncoding(th.nn.Module):
    '''
    https://pytorch.org/tutorials/beginner/transformer_tutorial.html
    '''
    def __init__(self, d_model: int,
            dropout: float = 0.1,
            max_len: int = 5000):
        super().__init__()
        self.dropout = th.nn.Dropout(p=dropout)
        position = th.arange(max_len).unsqueeze(1)
        div_term = th.exp(th.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = th.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = th.sin(position * div_term)
        pe[:, 0, 1::2] = th.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: th.Tensor) -> th.Tensor:
        '''
        x.shape = (seq_len, batch_size, embedding_dim)
        '''
        x = x + self.pe[:x.size(0)]
        return self.dropout(x)

class LongestPathTransformer(th.nn.Module):
    def __init__(self, model_type,
            input_size: int,
            d_model: int,
            nhead: int,
            d_mlp: int,
            nlayers: int,
            dropout: float = 0.1):
        super(LongestPathTransformer, self).__init__()
        self.model_type = model_type
        self.posenc = PositionalEncoding(d_model=d_model, dropout=dropout)
        enclayer = th.nn.TransformerEncoderLayer(d_model, nhead, d_mlp, dropout)
        self.transenc = th.nn.TransformerEncoder(enclayer, nlayers)
        self.encoder = th.nn.Linear(input_size, d_model) # XXX: replace into MLP
        self.d_model = d_model

        self.num_params = sum(param.numel() for param in self.parameters()
                if param.requires_grad)
    def forward_(self, src: th.Tensor, src_mask: th.Tensor):
        src = self.encoder(src) * math.sqrt(self.d_model)
        src = self.posenc(src)
        output = self.transenc(src, src_mask)
        return output
    def forward(self, x, y, z, *, device: str = 'cpu'):
        '''
        x is padded sequence
        y is labels
        z is EasyDict, keys:
            tc: translate and color info
            lens: sequence lengths
        '''
        B = int(x.shape[1])
        xe = self.encoder(x)
        print('debug', x.shape)
        raise NotImplementedError

class HierarchicalTransformer(object):
    ...

if __name__ == '__main__':
    console.rule('>_< testing position encoding')
    x = th.rand(10, 5, 32)
    posenc = PositionalEncoding(d_model=32)
    xpe = posenc(x)
    console.print('xpe.shape', xpe.shape)
