'''
https://lightning.ai/docs/pytorch/stable/notebooks/course_UvA-DL/11-vision-transformer.html
'''
import pytest
import torch as th
import rich
console = rich.get_console()


def image_to_patch(x, patch_size, flatten_channels=True):
    B, C, H, W = x.shape
    x = x.reshape(B, C, H // patch_size, patch_size,
                  W // patch_size, patch_size)
    x = x.permute(0, 2, 4, 1, 3, 5)  # [B, H', W', C, p_H, p_W]
    x = x.flatten(1, 2)  # B, H'*W', C, p_H, p_W
    if flatten_channels:
        x = x.flatten(2, 4)  # B, H'*W', C*p_H*p_W
    return x


def test_image_to_patch():
    images = th.rand(10, 3, 32, 32)  # CIFAR
    console.print('Original Images size', images.shape)

    images_seq = image_to_patch(images, 4)
    console.print('Image patches as a sequence', images_seq.shape)


class AttentionBlock(th.nn.Module):
    # Pre-LN attention block
    def __init__(self, embed_dim, hidden_dim, num_heads, dropout=0.0):
        super().__init__()

        self.layer_norm_1 = th.nn.LayerNorm(embed_dim)
        self.attn = th.nn.MultiheadAttention(embed_dim, num_heads)
        self.layer_norm_2 = th.nn.LayerNorm(embed_dim)
        self.linear = th.nn.Sequential(
            th.nn.Linear(embed_dim, hidden_dim),
            th.nn.GELU(),
            th.nn.Dropout(dropout),
            th.nn.Linear(hidden_dim, embed_dim),
            th.nn.Dropout(dropout),
        )

    def forward(self, x):
        res1 = self.layer_norm_1(x)
        res1 = self.attn(res1, res1, res1)[0]
        x = x + res1
        res2 = self.linear(self.layer_norm_2(x))
        x = x + res2
        return x


def test_attention_block():
    embed_dim = 256
    hidden_dim = 512
    num_heads = 8
    dropout = 0.2
    batch = 10
    seq_length = 64
    block = AttentionBlock(embed_dim, hidden_dim, num_heads, dropout)
    print(block)
    src = th.randn(seq_length, batch, embed_dim)  # batch_first=False
    print('src shape', src.shape)
    out = block(src)
    print('out shape', out.shape)


class ViT(th.nn.Module):
    def __init__(self, embed_dim, hidden_dim, num_channels,
                 num_heads, num_layers, num_classes, patch_size, num_patches,
                 dropout=0.0):
        super().__init__()
        self.patch_size = patch_size
        # layers
        self.input_layer = th.nn.Linear(num_channels * (patch_size**2), embed_dim)
        self.transformer = th.nn.Sequential(
            *(AttentionBlock(embed_dim, hidden_dim, num_heads, dropout)
            for _ in range(num_layers)))
        self.mlp_head = th.nn.Sequential(
            th.nn.LayerNorm(embed_dim),
            th.nn.Linear(embed_dim, num_classes)
            )
        self.dropout = th.nn.Dropout(dropout)
        # parameters
        self.cls_token = th.nn.Parameter(th.randn(1, 1, embed_dim))
        self.pos_embedding = th.nn.Parameter(th.randn(1, 1+num_patches, embed_dim))
    def forward(self, x):
        # preprocess
        src = image_to_patch(x, self.patch_size)
        B, T, _ = src.shape
        src = self.input_layer(src)
        # prepend the cls token and pos emb
        cls_token = self.cls_token.repeat(B, 1, 1)
        src = th.cat([cls_token, src], dim=1)
        src = src + self.pos_embedding[:, :T+1]
        # transformer
        src = self.dropout(src)
        src = src.transpose(0, 1)  # batch_first=False
        print('transformer: src', src.shape)
        out = self.transformer(src)
        print('transformer: out', out.shape)
        # classfication
        cls = self.mlp_head(out[0])
        return cls


def test_vit():
    images = th.rand(10, 3, 32, 32)
    embed_dim = 256
    hidden_dim = 512
    num_channels = 3
    num_heads = 8
    num_layers = 6
    num_classes = 10
    patch_size = 4
    num_patches = 64
    dropout = 0.2
    vit = ViT(embed_dim, hidden_dim, num_channels, num_heads, num_layers,
              num_classes, patch_size, num_patches, dropout)
    print(vit)
    print('images:', images.shape)
    output = vit(images)
    print('output:', output.shape)
