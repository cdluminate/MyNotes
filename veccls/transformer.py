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


if __name__ == '__main__':
    console.rule('>_< testing position encoding')
    x = th.rand(10, 5, 32)
    posenc = PositionalEncoding(d_model=32)
    xpe = posenc(x)
    console.print('xpe.shape', xpe.shape)
