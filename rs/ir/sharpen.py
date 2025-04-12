"""Sharpen (Unsharp Mask) a directory of images."""
import cv2
import argparse
import glob
import os
import concurrent.futures
import tqdm
import functools

def sharpen_image(image_path: str, output_path: str, sigma: float = 1.0, alpha: float = 1.0):
    # Read the image
    image = cv2.imread(image_path)
    basename = os.path.basename(image_path)

    # Apply Gaussian blur to create a blurred version of the image
    blurred = cv2.GaussianBlur(image, (0, 0), sigma)

    # Sharpen the image by combining the original and the blurred image
    sharpened = cv2.addWeighted(image, 1 + alpha, blurred, -alpha, 0)

    # Save the sharpened image
    dest = os.path.join(output_path, basename)
    cv2.imwrite(dest, sharpened)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', '-s', help='source directory', required=True)
    parser.add_argument('--dst', '-d', help='destination directory', required=True)
    parser.add_argument('--sigma', type=float, default=1.0, help='Gaussian blur sigma')
    parser.add_argument('--alpha', type=float, default=1.0, help='Sharpening strength')
    args = parser.parse_args()
    # Create destination directory if it doesn't exist
    os.makedirs(args.dst, exist_ok=True)
    # Get list of images
    images = glob.glob(os.path.join(args.src, '*.png'))
    images += glob.glob(os.path.join(args.src, '*.jpg'))
    images += glob.glob(os.path.join(args.src, '*.jpeg'))
    print('#images:', len(images))
    # worker function
    worker_fn = functools.partial(sharpen_image, output_path=args.dst, sigma=args.sigma, alpha=args.alpha)
    # Process images in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm.tqdm(executor.map(worker_fn, images), total=len(images)))