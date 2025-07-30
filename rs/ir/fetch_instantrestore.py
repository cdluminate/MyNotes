"""
Fetch the test subset from InstantRestore paper.
"""
import requests
import tarfile
import io
import argparse
import os
import shutil
import re

TARGZ = 'https://arxiv.org/src/2412.06753'

def savemember(member: tarfile.TarInfo, dest: str):
    """
    Save a member from a tarfile to a destination path.
    """
    fobj = tar.extractfile(member)
    with open(dest, 'wb') as out_f:
        shutil.copyfileobj(fobj, out_f)
    print(f'Extracted {member.name} to {dest}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='instantrestore_test')
    parser.add_argument('--cache', type=str, default='arXiv-2412.06753v1.tar.gz')
    args = parser.parse_args()

    # download the tar.gz file
    if not os.path.exists(args.cache):
        response = requests.get(TARGZ, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        with open(args.cache, 'wb') as f:
            f.write(response.content)
        fobj = io.BytesIO(response.content)
    else:
        fobj = open(args.cache, 'rb')

    # extract the images from tar.gz file
    os.makedirs(args.output, exist_ok=True)
    os.makedirs(os.path.join(args.output, 'lq'), exist_ok=True)
    os.makedirs(os.path.join(args.output, 'ref1'), exist_ok=True)
    os.makedirs(os.path.join(args.output, 'ref2'), exist_ok=True)
    os.makedirs(os.path.join(args.output, 'instantrestore'), exist_ok=True)

    with tarfile.open(fileobj=fobj, mode='r:gz') as tar:
        for member in tar.getmembers():
            #print(f'- {member.name}')

            # LQ images
            if member.name.startswith('images/common_people_results/inputs/'):
                dest = os.path.join(args.output, 'lq', os.path.basename(member.name))
                savemember(member, dest)
            
            # REF images
            elif member.name == 'images/common_people_results/references/assaf/IMG_0936.jpg':
                dest = os.path.join(args.output, 'ref1', 'assaf_2.jpg')
                savemember(member, dest)
            elif member.name == 'images/common_people_results/references/assaf/IMG_9721.jpg':
                dest = os.path.join(args.output, 'ref2', 'assaf_2.jpg')
                savemember(member, dest)

            elif member.name == 'images/common_people_results/references/dor/IMG-20240208-WA0054.jpg':
                dest = os.path.join(args.output, 'ref1', 'dor_6.jpg')
                savemember(member, dest)
            elif member.name == 'images/common_people_results/references/dor/IMG-20240208-WA0050.jpg':
                dest = os.path.join(args.output, 'ref2', 'dor_6.jpg')
                savemember(member, dest)
        
            elif member.name == 'images/common_people_results/references/gal/20220806_165757.jpg':
                dest = os.path.join(args.output, 'ref2', 'gal_0.jpg')
                savemember(member, dest)
            elif member.name == 'images/common_people_results/references/gal/20230812_170021.jpg':
                dest = os.path.join(args.output, 'ref1', 'gal_0.jpg')
                savemember(member, dest)

            elif member.name == 'images/common_people_results/references/saba/image_1.jpg':
                dest = os.path.join(args.output, 'ref1', 'saba_1.jpg')
                savemember(member, dest)
            elif member.name == 'images/common_people_results/references/saba/image_7.jpg':
                dest = os.path.join(args.output, 'ref2', 'saba_1.jpg')
                savemember(member, dest)

            elif member.name == 'images/common_people_results/references/shaked/IMG-20240209-WA0047.jpg':
                dest = os.path.join(args.output, 'ref1', 'shaked_0.jpg')
                savemember(member, dest)
                dest = os.path.join(args.output, 'ref1', 'shaked_5.jpg')
                savemember(member, dest)
            elif member.name == 'images/common_people_results/references/shaked/IMG-20240215-WA0004.jpg':
                dest = os.path.join(args.output, 'ref2', 'shaked_0.jpg')
                savemember(member, dest)
                dest = os.path.join(args.output, 'ref2', 'shaked_5.jpg')
                savemember(member, dest)
            
            elif member.name == 'images/common_people_results/references/shay/IMG-20240209-WA0012.jpg':
                dest = os.path.join(args.output, 'ref1', 'shay_8.jpg')
                savemember(member, dest)
            elif member.name == 'images/common_people_results/references/shay/IMG-20230821-WA0070.jpg':
                dest = os.path.join(args.output, 'ref2', 'shay_8.jpg')
                savemember(member, dest)

            elif member.name == 'images/common_people_results/references/shoam/IMG-20240209-WA0115.jpg':
                dest = os.path.join(args.output, 'ref1', 'shoam_8.jpg')
                savemember(member, dest)
            elif member.name == 'images/common_people_results/references/shoam/IMG-20240209-WA0118.jpg':
                dest = os.path.join(args.output, 'ref2', 'shoam_8.jpg')
                savemember(member, dest)

            elif member.name == 'images/common_people_results/references/tomer/IMG_1519.jpg':
                dest = os.path.join(args.output, 'ref1', 'tomer_0.jpg')
                savemember(member, dest)
            elif member.name == 'images/common_people_results/references/tomer/IMG_2322.jpg':
                dest = os.path.join(args.output, 'ref2', 'tomer_0.jpg')
                savemember(member, dest)

            # InstantRestore Results
            elif stub := re.match(r'images/common_people_results/ours_common_(.*)_(.*)_our\.jpg', member.name):
                dest = os.path.join(args.output, 'instantrestore', f'{stub.group(1)}_{stub.group(2)}.jpg')
                savemember(member, dest)

            else:
                pass