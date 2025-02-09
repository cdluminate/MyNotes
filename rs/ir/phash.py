'''
Calculate pHash for images, and cluster them with DBSCAN.
Requires both opencv-python and opencv-contrib-python packages.
'''
from typing import *
import os
import numpy as np
import cv2
import argparse
import rich
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import track
console = rich.get_console()


def calculate_single_image(path: str) -> np.ndarray:
    try:
        image = cv2.imread(path)
        if image is None:
            print(f'Error: Unable to read image {path}')
            return
        phash = cv2.img_hash.pHash(image)
        # This is a 64-bit hash, represented as a 8-element uint8 array.
        return phash.flatten()
    except Exception as e:
        print(f'Error processing image {path}: {e}')


def calculate_images(paths: list, jobs: int = 1) -> Dict[str, np.ndarray]:
    phashes = {}
    with ThreadPoolExecutor(max_workers=jobs) as executor:
        futures = [executor.submit(calculate_single_image, path) for path in paths]
        for path, future in track(zip(paths, as_completed(futures)), total=len(paths)):
            phashes[path] = future.result()
    return phashes


def hamming_distance(arr1: np.ndarray, arr2: np.ndarray) -> int:
    assert arr1.shape == arr2.shape == (8,)
    return np.count_nonzero(np.unpackbits(arr1) ^ np.unpackbits(arr2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate pHash for images.')
    parser.add_argument('image', type=str, help='Path to image or image directory')
    parser.add_argument('--jobs', '-j', type=int, default=1, help='Number of jobs to run in parallel')
    args = parser.parse_args()
    
    # Calculate pHash for images
    if os.path.isdir(args.image):
        paths = [os.path.join(args.image, f) for f in os.listdir(args.image) if f.endswith(('.jpg', '.png', '.jpeg'))]
    else:
        paths = [args.image]
    hashes = calculate_images(paths)
    console.print(hashes)

    # Calculate pairwise distances
    keys, values = zip(*list(hashes.items()))
    matrix = pairwise_distances(values, metric=hamming_distance)

    # Cluster with DBSCAN
    model = DBSCAN(eps=10, min_samples=2, metric='precomputed')
    clusters = model.fit_predict(matrix)
    console.print(Counter(clusters))
    group0 = [img for img, cluster in zip(keys, clusters) if cluster == 0]
    console.print(group0)
