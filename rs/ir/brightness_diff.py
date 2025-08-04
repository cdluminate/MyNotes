'''
Calculate brightness difference.
'''
import os
from PIL import Image
import argparse
import glob
import numpy as np


def get_brightness(image_path: str) -> float:
    img = Image.open(image_path).convert('HSV')
    h, s, v = img.split()
    del h, s  # We only need the value channel for brightness
    v = np.array(v)
    brightness = np.mean(v)
    return brightness


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True)
    parser.add_argument('--reference', type=str, required=True)
    parser.add_argument('--glob', type=str, default='*.png',
                        help='Glob pattern for image files in directory')
    args = parser.parse_args()

    if os.path.isdir(args.image):
        images = glob.glob(os.path.join(args.image, args.glob))
        for image in images:
            brightness = get_brightness(image)
            basename = os.path.basename(image)
            ref_path = os.path.join(args.reference, basename)
            ref_brightness = get_brightness(ref_path)
            print('Brightness-diff:', basename, abs(brightness - ref_brightness))
    else:
        brightness = get_brightness(args.image)
        basename = os.path.basename(args.image)
        ref_brightness = get_brightness(args.reference)
        print('Brightness-diff:', basename, abs(brightness - ref_brightness))

