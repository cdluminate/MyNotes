'''
Parallel PyIQA
https://github.com/chaofengc/IQA-PyTorch/blob/main/pyiqa/pyiqa_cmd.py
'''
from PIL import Image
import glob
import os
import concurrent.futures
import argparse
import re
import functools as ft
import rich
from pyiqa.api_helpers import create_metric
from rich.console import Console
from rich.status import Status
from rich.progress import track
console = Console(stderr=True)



def main(args):
    # read the list of images from args.target/args.glob
    list_images = glob.glob(os.path.join(args.target, args.glob))
    if len(list_images) == 0:
        if os.path.exists(args.target):
            list_images = [args.target]
        else:
            print('no images found')
            exit(0)
    print('#imgs:', len(list_images))

    # run the metrics one by one
    for metric in args.metrics:
        # load metrics
        with Status('Loading metrics...') as status:
            metric_func = create_metric(metric)
            status.update(f'Loaded {metric}')
        # only support NR metrics
        assert metric_func.metric_mode == 'NR'
        # run the metric
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
            results = list(track(ex.map(lambda x: metric_func(x).item(), list_images), total=len(list_images)))
        # dump the results
        for path, result in zip(list_images, results):
            print(path, metric, result)
            if args.dump:
                print(result, file=open(f'{path}.{metric}', 'wt'))
        # print the average
        print(metric, 'average:', sum(results) / len(results))



if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('metrics', nargs='*', type=str, help='metrics to run')
    ag.add_argument('--target', '-t', type=str, help='generated images')
    ag.add_argument('--glob', type=str, default='*.png', help='glob pattern')
    ag.add_argument('--dump', '-d', action='store_true', help='dump results to file')
    ag.add_argument('--jobs', '-j', type=int, default=8, help='number of jobs')
    ag.add_argument('--device', type=str, default=None, help='device')
    args = ag.parse_args()

    main(args)
