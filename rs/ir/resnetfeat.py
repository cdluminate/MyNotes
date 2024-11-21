import torch as th
import torchvision as V
from PIL import Image
import argparse
import numpy as np


def preprocess_image(path: str):
    img = Image.open(path)
    img = V.transforms.Resize(256)(img)
    img = V.transforms.CenterCrop(224)(img)
    img = V.transforms.ToTensor()(img)
    img = V.transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])(img)
    img = img.unsqueeze(0)
    return img


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image', type=str, nargs='+', help='image file')
    parser.add_argument('--device', type=str, default='mps', required=False)
    parser.add_argument('--ckpt', type=str, default=None, required=False)
    parser.add_argument('--suffix', type=str, default='.res50.npz', required=False)
    args = parser.parse_args()

    if args.ckpt is None:
        model = V.models.resnet50(pretrained=True)
        print('Loading Default Imagenet Pretrained Model')
    else:
        ckpt = th.load(args.ckpt, map_location=args.device)
        model = V.models.resnet50(pretrained=False)
        model.load_state_dict(ckpt)
        print('Loading Checkpoint', args.ckpt)
    model.fc = th.nn.Identity()
    model.eval()
    model = model.to(args.device)


    for img_path in args.image:
        img = preprocess_image(img_path)
        img = img.to(args.device)
        with th.no_grad():
            feat = model(img)
        feat = feat.view(-1)

        dest = img_path + args.suffix
        np.savez(dest, feat=feat.cpu().numpy())
        print(img_path, feat.shape, '->', dest)
