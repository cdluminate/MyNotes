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
                ref_mapping[row[0]] = row[2]
    return ref_mapping

def group_mappings(ref_mapping: Dict[str, List[str]]) -> List[List[str]]:
    '''
    Group mappings by reference image
    '''
    groups = []

    def _locate_group(key: str) -> List[str]:
        for group in groups:
            if key in group:
                return group
        newgroup = []
        groups.append(newgroup)
        return newgroup

    for k, v in ref_mapping.items():
        cursor = _locate_group(k)
        cursor.append(k)
        cursor.extend(eval(v))
        cursor = list(set(cursor))

    deduped = []
    for group in groups:
        deduped.append(list(set(group)))

    return deduped

def load_groups(csv_file: str) -> List[List[str]]:
    '''load groups from csv file'''
    mapping = load_ref_mapping(csv_file)
    #rich.print(mapping, len(mapping))
    groups = group_mappings(mapping)
    images = sum([len(x) for x in groups])
    print('Group', csv_file, 'images:', images, 'groups:', len(groups))
    if 'val_' in csv_file:
        assert (images, len(groups)) == (732, 300)
    if 'train_' in csv_file:
        assert (images, len(groups)) == (20125, 6403)
    if 'test_' in csv_file:
        assert (images, len(groups)) == (888, 157)
    return groups


def copy_files(src: str, groups: List[List[str]], dest: str) -> None:
    '''Copy files from source to destination'''
    for idx, group in enumerate(groups):
        for file in group:
            subdir = file[:2] + '000'
            src_file = os.path.join(src, subdir, file)
            if not os.path.exists(src_file):
                src_file = os.path.join(src, file)
            destdir = os.path.join(dest, str(idx))
            if not os.path.exists(destdir):
                os.makedirs(destdir)
            rich.print(src_file, '->', destdir)
            shutil.copy(src_file, destdir)

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
    train_groups = load_groups(os.path.join(args.ref, TRAIN_CSV))
    val_groups = load_groups(os.path.join(args.ref, VAL_CSV))
    test_groups = load_groups(os.path.join(args.ref, TEST_CSV))
    total = len(train_groups) + len(val_groups) + len(test_groups)
    print('Total groups:', total, 'train=', len(train_groups),
        'val=', len(val_groups), 'test=', len(test_groups))

    copy_files(args.src, train_groups, os.path.join(args.dst, 'train'))
    copy_files(args.src, val_groups, os.path.join(args.dst, 'val'))
    copy_files(args.src, test_groups, os.path.join(args.dst, 'test'))
