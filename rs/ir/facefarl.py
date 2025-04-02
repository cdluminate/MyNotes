'''Extract FARL features from face images.

https://github.com/faceperceiver/farl?tab=readme-ov-file
https://github.com/openai/CLIP/blob/main/clip/model.py
'''
import argparse
import torch
import clip
from PIL import Image
import numpy as np
import tqdm
import glob
import os


def load_model(args):
    model, preprocess = clip.load("ViT-B/16", device="cpu")
    model = model.to(args.device)
    farl_state = torch.load(args.ckpt, weights_only=True)
    model.load_state_dict(farl_state["state_dict"], strict=False)
    return model, preprocess


@torch.no_grad()
def farl_sequence(clip_model, image: torch.Tensor) -> torch.Tensor:
    # from CLIP.encode_image
    image: torch.Tensor = image.type(clip_model.dtype)
    visual = clip_model.visual
    # from VisionTransformer.forward
    x = visual.conv1(image)  # shape = [*, width, grid, grid]
    x = x.reshape(x.shape[0], x.shape[1], -1)  # shape = [*, width, grid ** 2]
    x = x.permute(0, 2, 1)  # shape = [*, grid ** 2, width]
    x = torch.cat([visual.class_embedding.to(x.dtype)
                   + torch.zeros(x.shape[0], 1, x.shape[-1], dtype=x.dtype, device=x.device),
                  x], dim=1)  # shape = [*, grid ** 2 + 1, width]
    x = x + visual.positional_embedding.to(x.dtype)
    x = visual.ln_pre(x)
    x = x.permute(1, 0, 2)  # NLD -> LND
    x = visual.transformer(x)
    x = x.permute(1, 0, 2)  # LND -> NLD
    #x = visual.ln_post(x[:, 0, :])
    #if visual.proj is not None:
    #    x = x @ visual.proj
    x = x.squeeze(0)  # (197, 768)
    return x

def encode_image(model, preprocess, image_path: str) -> np.ndarray:
    image_pil = Image.open(image_path)
    image = preprocess(image_pil).unsqueeze(0).to(args.device)
    image_features = farl_sequence(model, image)
    #with torch.no_grad():
    #    image_features = model.encode_image(image)  # clip embedding, not sequence
    return image_features.cpu().numpy()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu', help='Device to run model on')
    parser.add_argument('--ckpt', type=str, default='FaRL-Base-Patch16-LAIONFace20M-ep16.pth', help='Path to model checkpoint')
    parser.add_argument('--source', '-s', type=str, required=True, help='path to image directory')
    parser.add_argument('--glob', '-g', type=str, default='*.png', help='glob pattern')
    parser.add_argument('--destination', '-d', type=str, required=True, help='path to store outputs')
    args = parser.parse_args()

    images = glob.glob(os.path.join(args.source, args.glob))
    print('#images:', len(images))

    print('Loading model...')
    pack = load_model(args)
    os.makedirs(args.destination, exist_ok=True)

    for image in tqdm.tqdm(images):
        image_features = encode_image(*pack, image)
        #print(image_features.shape)
        image_name = os.path.basename(image)
        dest = os.path.join(args.destination, image_name.replace(args.glob[1:], '.npy'))
        np.save(dest, image_features)