'''
Inference commands for FFHQ-Ref images from Ref-LDM
https://github.com/ChiWeiHsiao/ref-ldm
'''
from typing import *
import os
import csv
import rich
import argparse
import shutil

TEST_CSV = 'reference_mapping/test_references.csv'
CMD_TEMPLATE = 'python inference.py --ddim_step 50 --lq_path {lq_path} --output_path {output_path} --ref_paths {ref_paths}'

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


def gen_cmds(test_mapping: Dict[str, List[str]], lq_path: str, ref_path: str, dst: str) -> List[str]:
    '''
    Generate commands for FFHQ dataset
    '''
    cmds = []
    for lq_image, ref_images in test_mapping.items():
        # Create output path
        output_path = os.path.join(dst, lq_image)
        os.makedirs(output_path, exist_ok=True)
        ref_images = eval(ref_images)
        ref_images = [os.path.join(ref_path, ref_image) for ref_image in ref_images]
        # Create command
        cmd = CMD_TEMPLATE.format(lq_path=os.path.join(lq_path, lq_image),
                                  output_path=output_path, ref_paths=ref_images[0])
        cmds.append(cmd)
    return cmds



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize FFHQ dataset by ID')
    parser.add_argument('--lq', type=str, default='FFHQ-Ref/test_images/moderate_degrad', help='Path to FFHQ dataset')
    parser.add_argument('--ref', type=str, default='FFHQ/images1024x1024', help='Path to save organized dataset')
    parser.add_argument('--dst', type=str, default='moderate_refldm')
    parser.add_argument('--csv', type=str, default='FFHQ-Ref', help='Path to FFHQ-Ref metadata')
    parser.add_argument('--output', type=str, default='')
    args = parser.parse_args()

    # Load reference mapping
    test_mapping = load_ref_mapping(os.path.join(args.csv, TEST_CSV))
    print('Test Images:', len(test_mapping))

    # Generate commands
    cmds = gen_cmds(test_mapping, args.lq, args.ref, args.dst)
    if args.output:
        with open(args.output, 'w') as f:
            for cmd in cmds:
                f.write(cmd + '\n')
    else:
        rich.print('Test Commands:', cmds)
