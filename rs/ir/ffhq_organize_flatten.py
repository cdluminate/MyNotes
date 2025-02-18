'''
Script for groupping FFHQ-Ref images from Ref-LDM
https://github.com/ChiWeiHsiao/ref-ldm
'''
from typing import *
import os
import csv
import rich
import argparse
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

TRAIN_CSV = 'reference_mapping/train_references.csv'
VAL_CSV = 'reference_mapping/val_references.csv'
TEST_CSV = 'reference_mapping/test_references.csv'

def load_ref_mapping(csv_file: str) -> Dict[str, List[str]]:
    '''
    Load reference mappings from CSV file
    '''
    # Format: gt_image, lq_image, ref_image
    ref_mapping = {}
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader) # Skip header
        if 'train_' in csv_file:
            for row in reader:
                ref_mapping[row[0]] = row[1]
        else:
            for row in reader:
                ref_mapping[row[0]] = row[2]
    return ref_mapping


def flatten_images(src: str, mappings: Dict[str, List[str]], dest: str, resize: int) -> None:

    def _worker(src_path: str, dest_path: str, resize: int) -> None:
        img = Image.open(src_path).convert('RGB')
        img = img.resize((resize, resize), resample=Image.Resampling.BICUBIC)
        os.mkdir(os.path.dirname(dest_path), exist_ok=True)
        img.save(dest_path, format='PNG')
        rich.print(src_path, f'->({resize})->', dest_path)

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as ex:
        for input_image, references in mappings.items():
            # copy the input image
            print('DEBUG:',
                  os.path.join(src, input_image),
                  os.path.join(dest, 'input', input_image),
                  resize) if False else None
            ex.submit(_worker,
                      os.path.join(src, input_image),
                      os.path.join(dest, 'input', input_image),
                      resize,
            )
            references = eval(references) # stringified list
            for i, file in enumerate(references):
                print('DEBUG:',
                      os.path.join(src, file),
                      os.path.join(dest, f'ref{i}', input_image),
                      resize) if False else None
                ex.submit(_worker,
                          os.path.join(src, file),
                          os.path.join(dest, f'ref{i}', input_image),
                          resize)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize FFHQ dataset, flattened.')
    parser.add_argument('--src', type=str, default='FFHQ/images1024x1024', help='Path to FFHQ dataset')
    parser.add_argument('--dst', type=str, required=True, help='Path to save organized dataset')
    parser.add_argument('--ref', type=str, default='FFHQ-Ref', help='Path to FFHQ-Ref metadata')
    parser.add_argument('--resize', type=int, default=512, help='Resize images')
    parser.add_argument('--jobs', type=int, default=os.cpu_count(), help='Number of jobs')
    args = parser.parse_args()

    # training
    os.makedirs(os.path.join(args.dst, 'train'), exist_ok=True)
    train_groups = load_ref_mapping(os.path.join(args.ref, TRAIN_CSV))
    flatten_images(args.src, train_groups, os.path.join(args.dst, 'train'), args.resize)

    #os.makedirs(os.path.join(args.dst, 'val'), exist_ok=True)
    #os.makedirs(os.path.join(args.dst, 'test'), exist_ok=True)

    # Load reference mapping

    #val_groups = load_ref_mapping(os.path.join(args.ref, VAL_CSV))
    #test_groups = load_ref_mapping(os.path.join(args.ref, TEST_CSV))

    # flattening directories

    #copy_files(args.src, val_groups, os.path.join(args.dst, 'val'))
    #copy_files(args.src, test_groups, os.path.join(args.dst, 'test'))
