'''
Apply Gaussian blur on image directory and save PNG.
'''
from PIL import Image, ImageFilter
import glob
import os
import concurrent.futures
import argparse
import re
import functools as ft


def force_png_extension(text):
    return re.sub(r'\.(jpg|png)$', '.png', text, flags=re.IGNORECASE)


def gaussian_blur(image, size=0):
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=size))
    return blurred_image


def _worker(pack, destdir: str = 'test__', size: int = 0, total: int = -1):
    # unpack the argument tuple
    i, path = pack
    # read image and upscale
    img = Image.open(path).convert('RGB')
    img = gaussian_blur(img, size=size)
    # figure out dest path and force png extension
    name = os.path.basename(path)
    dest = os.path.join(destdir, name)
    dest = force_png_extension(dest)
    # save and show progress
    img.save(dest, format='PNG')
    print(i+1, '/', total, path, '->', dest)
    return dest


def main(args):
    # read the list of images from args.src/args.glob
    list_images = glob.glob(os.path.join(args.src, args.glob))
    print('#imgs:', len(list_images))

    # prepare output directory
    if not os.path.exists(args.dst):
        os.makedirs(args.dst)

    # do it in parallel
    worker = ft.partial(_worker,
                        destdir=args.dst,
                        size=args.size,
                        total=len(list_images))
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        results = ex.map(worker, enumerate(list_images))
    results = list(results)
    print('Finished', len(results))


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--src', '-s', help='source directory',
                    type=str, required=True)
    ag.add_argument('--glob', '-g', help='glob pattern',
                    type=str, default='*.png')
    ag.add_argument('--dst', '-d', help='destination directory',
                    type=str, required=True)
    ag.add_argument('--jobs', '-j', help='parallelism', type=int, default=8)
    ag.add_argument('--size', help='gaussian kernel size',
                    type=int, default=0)
    args = ag.parse_args()

    main(args)
