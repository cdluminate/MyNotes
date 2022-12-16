#!/usr/bin/env python3
import sys, os, yaml, re
import numpy as np
import torch as th, torch.utils.data
import argparse, collections
from tqdm import tqdm
import lib
from termcolor import cprint, colored
import matplotlib.pyplot as plt
import sklearn


def Factor(argv):
    '''
    Factorize Adversarial Perturbations
    '''
    ag = argparse.ArgumentParser()
    ag.add_argument('-D', '--device', type=str,
            default='cuda' if th.cuda.is_available() else 'cpu')
    ag.add_argument('-F', '--factorization', type=str, required=True,
            choices=['untarget', 'coarse', 'fine'])
    ag.add_argument('-e', '--epsilon', type=float, default=4./255.)
    ag.add_argument('-M', '--model', type=str, required=True)
    ag.add_argument('--pgditer', type=int, default=128)
    ag = ag.parse_args(argv)

    # Dump configurations
    cprint('>_< Dumping arguments and Loading configs', 'white', 'on_blue')
    print(yaml.dump(vars(ag)))
    with open('config.yml', 'rt') as f:
        config = yaml.load(f.read(), Loader=yaml.SafeLoader)

    # Load the model
    cprint('>_< Initializing model', 'white', 'on_blue')
    Mname, Mpath = ag.model, 'trained/' + ag.model + '.sdth'
    model = getattr(lib, Mname).Model().to(ag.device)
    model.load_state_dict(th.load(Mpath))

    # Load the dataset
    cprint('>_< Loading dataset', 'white', 'on_blue')
    loader_test = model.getloader('test', config[Mname]['batchsize_atk'])

    for I, (images, labels) in enumerate(loader_test):
        cprint(f'- [ {I} ] -----------------------', 'red')
        images, labels = images.to(ag.device), labels.view(-1).to(ag.device)
        _factor_batch(model, images, labels, ag)
        exit(0)


def _factor_batch(model, images, labels, ag):
    # evaluate model on original examples
    with th.no_grad():
        output = model.forward(images)
        acc_orig = output.max(1)[1].eq(labels).sum().item()/len(labels)
        print(colored('** orig accuracy', 'green'), acc_orig)

    # (8/255 ~ 0.031) https://arxiv.org/pdf/1706.06083.pdf
    model.eval()
    xr, r = lib.attacks.projectedGradientDescent(model, images, labels,
            eps=ag.epsilon, alpha=1./255., maxiter=ag.pgditer, verbose=True,
            device=ag.device, targeted=False, unbound=False, rinit=False)
    with th.no_grad():
        output = model.forward(xr)
        acc_pgd = output.max(1)[1].eq(labels).sum().item()/len(labels)
        labels_pgd = output.max(1)[1].detach().cpu().flatten().numpy()
        print(colored('** pgd accuracy', 'green'), acc_pgd)
    model.eval()
    xrg, rg = lib.attacks.projectedGradientDescent(model, images, labels,
            eps=ag.epsilon, alpha=1./255., maxiter=ag.pgditer, verbose=True,
            device=ag.device, targeted=False, unbound=False, rinit=False, B_UAP=True)
    with th.no_grad():
        output = model.forward(xrg)
        acc_uap = output.max(1)[1].eq(labels).sum().item()/len(labels)
        labels_uap = output.max(1)[1].detach().cpu().flatten().numpy()
        print(colored('** uap accuracy', 'green'), acc_uap)

    # factor
    diff = (r - rg).detach().cpu().view(images.size(0), -1).numpy()
    npxr = xr.detach().cpu().view(images.size(0),-1).numpy()
    npr  =  r.detach().cpu().view(images.size(0),-1).numpy()
    nprg = rg.detach().cpu().view(images.size(0),-1).numpy()
    npimg = images.detach().cpu().view(images.size(0),-1).numpy()
    marker = '.'

    print('Diff.shape:', diff.shape)
    labels = labels.cpu().flatten().numpy()
    plt.figure()

    plt.subplot(2,5,1)
    embs = sklearn.manifold.TSNE(n_components=2, verbose=1).fit_transform(npimg)
    plt.scatter(embs[:,0], embs[:,1], marker=marker, c=labels, cmap='gist_rainbow')
    plt.colorbar()
    plt.title('npimg labels')

    plt.subplot(2,5,2)
    embs = sklearn.manifold.TSNE(n_components=2, verbose=1).fit_transform(npxr)
    plt.scatter(embs[:,0], embs[:,1], marker=marker, c=labels, cmap='gist_rainbow')
    plt.colorbar()
    plt.title('npxr labels')

    plt.subplot(2,5,3)
    embs = sklearn.manifold.TSNE(n_components=2, verbose=1).fit_transform(diff)
    plt.scatter(embs[:,0], embs[:,1], marker=marker, c=labels, cmap='gist_rainbow')
    plt.colorbar()
    plt.title('diff labels')

    plt.subplot(2,5,4)
    embs = sklearn.manifold.TSNE(n_components=2, verbose=1).fit_transform(npr)
    plt.scatter(embs[:,0], embs[:,1], marker=marker, c=labels, cmap='gist_rainbow')
    plt.colorbar()
    plt.title('npr labels')

    plt.subplot(2,5,5)
    embs = sklearn.manifold.TSNE(n_components=2, verbose=1).fit_transform(nprg)
    plt.scatter(embs[:,0], embs[:,1], marker=marker, c=labels, cmap='gist_rainbow')
    plt.colorbar()
    plt.title('nprg labels')

    plt.subplot(2,5,6)
    embs = sklearn.manifold.TSNE(n_components=2, verbose=1).fit_transform(npxr)
    plt.scatter(embs[:,0], embs[:,1], marker=marker, c=labels_pgd, cmap='gist_rainbow')
    plt.colorbar()
    plt.title('npxr labels_pgd')

    plt.subplot(2,5,7)
    embs = sklearn.manifold.TSNE(n_components=2, verbose=1).fit_transform(npimg)
    plt.scatter(embs[:,0], embs[:,1], marker=marker, c=labels_pgd, cmap='gist_rainbow')
    plt.colorbar()
    plt.title('npimg labels_pgd')

    plt.subplot(2,5,8)
    embs = sklearn.manifold.TSNE(n_components=2, verbose=1).fit_transform(diff)
    plt.scatter(embs[:,0], embs[:,1], marker=marker, c=labels_pgd, cmap='gist_rainbow')
    plt.colorbar()
    plt.title('diff labels_pgd')

    plt.subplot(2,5,9)
    embs = sklearn.manifold.TSNE(n_components=2, verbose=1).fit_transform(npr)
    plt.scatter(embs[:,0], embs[:,1], marker=marker, c=labels_pgd, cmap='gist_rainbow')
    plt.colorbar()
    plt.title('npr labels_pgd')

    plt.subplot(2,5,10)
    embs = sklearn.manifold.TSNE(n_components=2, verbose=1).fit_transform(nprg)
    plt.scatter(embs[:,0], embs[:,1], marker=marker, c=labels_pgd, cmap='gist_rainbow')
    plt.colorbar()
    plt.title('nprg labels_pgd')

    plt.tight_layout()
    #plt.savefig('_factor.svg')
    plt.show()

if __name__ == '__main__':
    Factor(sys.argv[1:])
