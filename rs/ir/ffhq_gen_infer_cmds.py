'''
Inference commands for FFHQ-Ref images for Ref-LDM, RestoreID
https://github.com/ChiWeiHsiao/ref-ldm
https://github.com/YingJiacheng/RestorerID
'''
from typing import *
import os
import csv
import rich
import argparse
import shutil

TEST_CSV = 'reference_mapping/test_references.csv'
CMD_TEMPLATE = 'python inference.py --ddim_step 50 --lq_path {lq_path} --output_path {output_path} --ref_paths {ref_paths}'
CMD_TEMPLATE_RESTOREID = 'python scripts/Inference.py --LQpath {lq_path} --Outputpath {output_path} --Refpath {ref_paths}'

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


def gen_cmds(test_mapping: Dict[str, List[str]], lq_path: str, ref_path: str, dst: str, *, variant: str = 'refldm', num_ref: int = 1) -> List[str]:
    '''
    Generate commands for FFHQ dataset
    '''
    cmds = ['set -x']

    # load template
    if variant == 'refldm':
        template = CMD_TEMPLATE
    elif variant == 'restoreid':
        template = CMD_TEMPLATE_RESTOREID
    else:
        raise ValueError('Unknown variant')
    
    for lq_image, ref_images in test_mapping.items():
        # Create output path
        if variant == 'refldm':
            output_path = os.path.join(dst, lq_image)
        elif variant == 'restoreid':
            output_path = dst
        else:
            raise ValueError('Unknown variant')
        os.makedirs(output_path, exist_ok=True)
        ref_images = eval(ref_images)
        ref_images = [os.path.join(ref_path, ref_image) for ref_image in ref_images]
        # Create command
        real_refs = []
        if False:
            # for CelebA-Ref-Test
            for tmp in ref_images:
                if os.path.exists(tmp):
                    real_refs.append(tmp)
        else:
            # for FFHQ-Ref Test
            real_refs = ref_images
        if not real_refs:
            real_ref = '!not-available!'
        elif num_ref == 1:
            real_ref = real_refs[0]
        else:
            tmp2 = []
            for i in range(1, num_ref + 1):
                idx = min(len(real_refs) - 1, i - 1)
                tmp2.append(real_refs[i])
            real_ref = ' '.join(tmp2)
        # for FFHQ-Ref, real_ref is the first image.
        # for CelebA-Ref-Test, real_ref is not necessarily the first image.
        cmd = template.format(lq_path=os.path.join(lq_path, lq_image),
                                  output_path=output_path, ref_paths=real_ref)
        if len(real_refs) > 0:
            cmds.append(cmd)
        else:
            cmds.append('# ' + cmd)
    return cmds



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize FFHQ dataset by ID')
    parser.add_argument('--lq', type=str, default='FFHQ-Ref/test_images/moderate_degrad', help='Path to FFHQ dataset')
    parser.add_argument('--ref', type=str, default='FFHQ/images1024x1024', help='Path to save organized dataset')
    parser.add_argument('--dst', type=str, default='moderate_refldm')
    parser.add_argument('--csv', type=str, default='FFHQ-Ref', help='Path to FFHQ-Ref metadata')
    parser.add_argument('--output', type=str, default='')
    parser.add_argument('--variant', type=str, default='refldm', choices=['refldm', 'restoreid'])
    parser.add_argument('--num_ref', type=int, default=1, help='Number of references to use')
    args = parser.parse_args()

    # Check if args are valid
    if args.variant == 'restoreid':
        assert args.num_ref == 1, 'RestoreID only supports one reference image'

    # Load reference mapping
    test_mapping = load_ref_mapping(os.path.join(args.csv, TEST_CSV))
    print('Test Images:', len(test_mapping))

    # Generate commands
    cmds = gen_cmds(test_mapping, args.lq, args.ref, args.dst, variant=args.variant, num_ref=args.num_ref)
    if args.output:
        with open(args.output, 'w') as f:
            for cmd in cmds:
                f.write(cmd + '\n')
    else:
        rich.print('Test Commands:', cmds)
