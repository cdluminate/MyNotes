'''
nlinsp
'''
import numpy as np
import torch as th
import pandas as pd
import timm
import argparse
import matplotlib.pyplot as plt
import rich
console = rich.get_console()


_RESULTS_CSV_URL_ = 'https://github.com/huggingface/pytorch-image-models/raw/main/results/results-imagenet.csv'


def list_pretrained_models():
    '''
    show the top1 vs param_count plot
    '''
    list_models = timm.list_models(pretrained=True)
    results = pd.read_csv(_RESULTS_CSV_URL_)
    #import IPython
    #IPython.embed(colors='neutral')
    param_count = []
    top1 = []
    for name in list_models:
        row = results.loc[results['model'] == name]
        assert len(row) <= 1
        if len(row) == 0:
            continue
        #console.print(row)
        param_count.append(float(row.param_count.values[0]))
        top1.append(float(row.top1.values[0]))
    #param_count = np.array(param_count)
    #top1 = np.array(top1)
    #print(top1)
    #argsort = param_count.argsort()
    #param_count = param_count[argsort]
    #top1 = top1[argsort]
    ax = plt.figure(figsize=(8,5)).gca()
    ax.scatter(param_count, top1)
    #ax.set_xticks(ax.get_xticks()[::20])
    ax.set_title('Top-1 v.s. param_count')
    ax.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--list-pretrained-models', action='store_true')
    ag = ag.parse_args()

    if ag.list_pretrained_models:
        list_pretrained_models()
