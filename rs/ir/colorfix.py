'''
https://github.com/IceClear/StableSR/raw/refs/heads/main/scripts/wavelet_color_fix.py
'''

import torch
from PIL import Image
from torch import Tensor
from torch.nn import functional as F
import functools as ft
import glob
import argparse
import os
import concurrent.futures

from torchvision.transforms import ToTensor, ToPILImage

def adain_color_fix(target: Image, source: Image):
    # Convert images to tensors
    to_tensor = ToTensor()
    target_tensor = to_tensor(target).unsqueeze(0)
    source_tensor = to_tensor(source).unsqueeze(0)

    # Apply adaptive instance normalization
    result_tensor = adaptive_instance_normalization(target_tensor, source_tensor)

    # Convert tensor back to image
    to_image = ToPILImage()
    result_image = to_image(result_tensor.squeeze(0).clamp_(0.0, 1.0))

    return result_image

def wavelet_color_fix(target: Image, source: Image):
    # Convert images to tensors
    to_tensor = ToTensor()
    target_tensor = to_tensor(target).unsqueeze(0)
    source_tensor = to_tensor(source).unsqueeze(0)

    # Apply wavelet reconstruction
    result_tensor = wavelet_reconstruction(target_tensor, source_tensor)

    # Convert tensor back to image
    to_image = ToPILImage()
    result_image = to_image(result_tensor.squeeze(0).clamp_(0.0, 1.0))

    return result_image

def calc_mean_std(feat: Tensor, eps=1e-5):
    """Calculate mean and std for adaptive_instance_normalization.
    Args:
        feat (Tensor): 4D tensor.
        eps (float): A small value added to the variance to avoid
            divide-by-zero. Default: 1e-5.
    """
    size = feat.size()
    assert len(size) == 4, 'The input feature should be 4D tensor.'
    b, c = size[:2]
    feat_var = feat.reshape(b, c, -1).var(dim=2) + eps
    feat_std = feat_var.sqrt().reshape(b, c, 1, 1)
    feat_mean = feat.reshape(b, c, -1).mean(dim=2).reshape(b, c, 1, 1)
    return feat_mean, feat_std

def adaptive_instance_normalization(content_feat:Tensor, style_feat:Tensor):
    """Adaptive instance normalization.
    Adjust the reference features to have the similar color and illuminations
    as those in the degradate features.
    Args:
        content_feat (Tensor): The reference feature.
        style_feat (Tensor): The degradate features.
    """
    size = content_feat.size()
    style_mean, style_std = calc_mean_std(style_feat)
    content_mean, content_std = calc_mean_std(content_feat)
    normalized_feat = (content_feat - content_mean.expand(size)) / content_std.expand(size)
    return normalized_feat * style_std.expand(size) + style_mean.expand(size)

def wavelet_blur(image: Tensor, radius: int):
    """
    Apply wavelet blur to the input tensor.
    """
    # input shape: (1, 3, H, W)
    # convolution kernel
    kernel_vals = [
        [0.0625, 0.125, 0.0625],
        [0.125, 0.25, 0.125],
        [0.0625, 0.125, 0.0625],
    ]
    kernel = torch.tensor(kernel_vals, dtype=image.dtype, device=image.device)
    # add channel dimensions to the kernel to make it a 4D tensor
    kernel = kernel[None, None]
    # repeat the kernel across all input channels
    kernel = kernel.repeat(3, 1, 1, 1)
    image = F.pad(image, (radius, radius, radius, radius), mode='replicate')
    # apply convolution
    output = F.conv2d(image, kernel, groups=3, dilation=radius)
    return output

def wavelet_decomposition(image: Tensor, levels=5):
    """
    Apply wavelet decomposition to the input tensor.
    This function only returns the low frequency & the high frequency.
    """
    high_freq = torch.zeros_like(image)
    for i in range(levels):
        radius = 2 ** i
        low_freq = wavelet_blur(image, radius)
        high_freq += (image - low_freq)
        image = low_freq

    return high_freq, low_freq

def wavelet_reconstruction(content_feat:Tensor, style_feat:Tensor):
    """
    Apply wavelet decomposition, so that the content will have the same color as the style.
    """
    # calculate the wavelet decomposition of the content feature
    content_high_freq, content_low_freq = wavelet_decomposition(content_feat)
    del content_low_freq
    # calculate the wavelet decomposition of the style feature
    style_high_freq, style_low_freq = wavelet_decomposition(style_feat)
    del style_high_freq
    # reconstruct the content feature with the style's high frequency
    return content_high_freq + style_low_freq


def main(args):
    # read the list of images from args.src/args.glob
    list_images = glob.glob(os.path.join(args.src, args.glob))
    print('#imgs:', len(list_images))

    # check if all reference images are available
    def _check_image(srcpath, args) -> bool:
        fname = os.path.basename(srcpath)
        refpath = os.path.join(args.ref, fname)
        if not os.path.exists(refpath):
            print('Reference image not found:', refpath)
            return False
        return True
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        results = ex.map(ft.partial(_check_image, args=args), list_images)
    results = list(results)
    assert all(results), 'Some reference images are missing'

    # prepare output directory
    if not os.path.exists(args.dst):
        os.makedirs(args.dst)

    # colorfix worker function
    def _worker(pack, args, total: int = -1):
        # unpack the argument tuple
        (i, srcpath) = pack
        fname = os.path.basename(srcpath)
        refpath = os.path.join(args.ref, fname)
        destpath = os.path.join(args.dst, fname)
        # read image and upscale
        img = Image.open(srcpath).convert('RGB')
        refimg = Image.open(refpath).convert('RGB')
        if args.method == 'adain':
            dest = adain_color_fix(img, refimg)
        elif args.method == 'wavelet':
            dest = wavelet_color_fix(img, refimg)
        else:
            raise ValueError('Unknown method:', args.method)
        # save and show progress
        dest.save(destpath, format='PNG')
        print(i+1, '/', total, srcpath, '->[adain]->', destpath)
        return dest

    # do it in parallel
    worker = ft.partial(_worker, args=args, total=len(list_images))
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        results = ex.map(worker, enumerate(list_images))
    results = list(results)
    print('Finished', len(results))


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--src', '-s', help='source directory',
                    type=str, required=True)
    ag.add_argument('--ref', '-r', help='reference image',
                    type=str, required=True)
    ag.add_argument('--glob', '-g', help='glob pattern',
                    type=str, default='*.png')
    ag.add_argument('--dst', '-d', help='destination directory',
                    type=str, required=True)
    ag.add_argument('--jobs', '-j', help='parallelism',
                    type=int, default=8)
    ag.add_argument('--method', help='colorfix method',
                    type=str, default='adain', choices=['adain', 'wavelet'])
    args = ag.parse_args()

    main(args)
