from typing import *
import os
import csv
import rich
import argparse
from collections import Counter

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
                ref_mapping[row[0]] = eval(row[1])
        else:
            for row in reader:
                ref_mapping[row[0]] = eval(row[2])
    return ref_mapping

def csv_stat(file_path: str):
    mapping = load_ref_mapping(file_path)
    rich.print('Dataset size:', len(mapping))
    ct = Counter(len(v) for v in mapping.values())
    rich.print('Number of references per image:', ct)
    assert( len(mapping) == sum(ct.values()) ), 'Total references do not match dataset size'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FFHQ Reference Statistics')
    parser.add_argument('--root', type=str, default='FFHQ-Ref', help='Root directory of FFHQ dataset')
    args = parser.parse_args()

    for csv_file in [TRAIN_CSV, VAL_CSV, TEST_CSV]:
        csv_path = os.path.join(args.root, csv_file)
        print(f'Statistics for {csv_file}:')
        csv_stat(csv_path)