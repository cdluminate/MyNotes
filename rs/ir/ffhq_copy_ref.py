'''
Script for groupping FFHQ-Ref images from Ref-LDM
https://github.com/ChiWeiHsiao/ref-ldm
'''
from typing import *
import os
import csv
import rich
import argparse
import shutil

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
                assert row[0] == row[1]
                ref_mapping[row[0]] = row[2]
    return ref_mapping

def copy_files(src: str, ref_mapping: Dict[str, List[str]], dest: str) -> None:
    '''Copy files from source to destination'''
    for (lq, ref_images) in ref_mapping.items():
        src_file = os.path.join(src, lq)
        for (idx, ref_image) in enumerate(ref_images):
            subdir = os.path.join(dest, 'ref' + str(idx+1))
            os.makedirs(subdir, exist_ok=True)
            dest_file = os.path.join(subdir, lq)
            rich.print(src_file, '->', dest_file)
            shutil.copy(src_file, dest_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize FFHQ dataset by ID')
    parser.add_argument('--src', type=str, default='FFHQ/images1024x1024', help='Path to FFHQ dataset')
    parser.add_argument('--dst', type=str, required=True, help='Path to save organized dataset')
    parser.add_argument('--ref', type=str, default='FFHQ-Ref', help='Path to FFHQ-Ref metadata')
    args = parser.parse_args()

    # Create directories
    if not os.path.exists(args.dst):
        os.makedirs(args.dst)
        os.makedirs(os.path.join(args.dst, 'train'))
        os.makedirs(os.path.join(args.dst, 'val'))
        os.makedirs(os.path.join(args.dst, 'test'))

    # Load reference mapping
    #train_groups = load_groups(os.path.join(args.ref, TRAIN_CSV))
    #copy_files(args.src, train_groups, os.path.join(args.dst, 'train'))
    #val_groups = load_groups(os.path.join(args.ref, VAL_CSV))
    #copy_files(args.src, val_groups, os.path.join(args.dst, 'val'))

    test_refs = load_ref_mapping(os.path.join(args.ref, TEST_CSV))
    print('Test refs:', len(test_refs))
    copy_files(args.src, test_groups, os.path.join(args.dst, 'test'))
