#
# <<< NeuroSki Library >>>
#
from scipy import stats
from sklearn.decomposition import PCA, FastICA, NMF, TruncatedSVD
from sklearn.manifold import TSNE, Isomap, MDS, LocallyLinearEmbedding
from termcolor import cprint, colored
from tqdm import tqdm
import collections
import functools
import math
import numpy as np
import os, sys, re
import pylab as lab
import random
import statistics
import torch as th
import traceback
import json
from .utils import IMmean, IMstd, renorm, denorm, xdnorm
from .attacks import carliniAndWagner, projectedGradientDescent

###########################################################################

def cls_neuroski(model, skitype, loader, *, dconf, device, verbose=False):
    from collections import defaultdict
    stats = defaultdict(list)
    for N, (images, labels) in enumerate(loader):
        cprint(f'>_< NeuroSki Progress ({N+1} / {len(loader)})'.rjust(72), 'white', 'on_green')
        # do the job
        if skitype == 'NS:VAL':
            # Validate the core assumption of NeuroSki
            stat = NeuroSkiValidate(model, images, labels, dconf=dconf, verbose=verbose, device=device)
        elif skitype == 'NS:ZREG':
            stat = NeuroSkiZigRegression(model, images, labels, dconf=dconf, verbose=verbose, device=device)
        elif skitype == 'NS:FRAC':
            raise NotImplementedError
        else:
            raise Exception(f"does not recognize {skitype}")
        # collect stats
        for (k, v) in stat.items():
            stats[k].append(v)
        if verbose:
            print(json.dumps(stat, indent=2))
    cprint('>_< Summary', 'red', 'on_white')
    print(colored(json.dumps({k:np.mean(v) for (k,v) in stats.items()}, indent=2), 'cyan', None, ['bold']))
    print(' NS_ATK  |', os.getenv('NS_ATK', 'N/A'))
    print('epsilon  |', dconf['epsilon'])
    print('maxiter  |', dconf['maxiter'])
    print('nsmaxite |', dconf['nsmaxiter'])

#########################################################################


def neuroSki(model, images, labels, *, eps=0.0, alpha=0.0,
        maxiter=24, verbose=False, device='cpu', targeted=True, unbound=True,
        maxiterT=0):
    '''
    do the zig-zag (indented) attacking process
    input is images and the corresponding labels
    output is the trajectories
    there are targeted neuroski and untargeted neuroski.

    NOTE: the untargeted neuroski is not working well. use targeted as default

    In untargeted neuroski, benign examples usually have larger ski distance
    compared to that of the adversarial examples. Plus, by observing the trajectories,
    I found no clear evidence to differentiate benign examples and adversarial examples.
    '''
    assert(type(images) == th.Tensor)
    assert(eps is not None)
    _iseven = lambda x: bool((x%2)==0)
    NS_DEF = str(os.getenv('NS_DEF', 'PGD'))
    # prepare
    images = images.to(device).clone().detach()
    images_orig = images.clone().detach()
    images.requires_grad = True
    labels = labels.to(device).view(-1)
    traj = [images_orig.clone()]
    label_ubound = None
    # start attack
    model.eval()
    for iteration in range(maxiter):
        # model.train()  ## do we need it?
        # setup optimizers, and clear the gradient
        optim = th.optim.SGD(model.parameters(), lr=0.)
        optim.zero_grad()
        optimx = th.optim.SGD([images], lr=1.)
        optimx.zero_grad()
        # forward
        if not targeted:
            # untargeted neuroski
            output, loss = model.loss(images, labels, adv=False)
            if _iseven(iteration):
                loss = -loss  # attack: gradient ascent
            else:
                loss = loss # reset: gradient descent
        else:
            # targeted neuroski (*)
            if label_ubound is None:
                output, _ = model.loss(images, labels, adv=False)
                label_ubound = output.shape[1]
            if _iseven(iteration):
                # attack: gradient descent on fake label
                rlabels = th.randint_like(labels, 0, label_ubound, device=labels.device)
                for i in range(len(rlabels)):
                    if rlabels[i] == labels[i]:
                        while rlabels[i] == labels[i]:
                            rlabels[i] = th.randint(0, label_ubound, (1,))
                    else:
                        continue
                #print('labels == rlabels?', labels == rlabels)
                output, loss = model.loss(images, rlabels, adv=False)
                #print(rlabels[:7]) # debug use
            else:
                # reset: gradient descient on true label
                output, loss = model.loss(images, labels, adv=False)
                #print(labels[:7]) # debug use
        loss.backward()
        # dispatch attack_step
        if NS_DEF == 'PGD':
            if images_orig.min() >= 0. and images_orig.max() <= 1.:
                images.grad.data.copy_(alpha * th.sign(images.grad))
            elif images_orig.min() < 0.:
                images.grad.data.copy_((alpha/IMstd[:,None,None]).to(device) * th.sign(images.grad))
            else:
                raise Exception
        elif NS_DEF == 'FGSM':
            if images_orig.min() >= 0. and images_orig.max() <= 1.:
                images.grad.data.copy_(eps * th.sign(images.grad))
            elif images_orig.min() < 0.:
                raise Exception
            else:
                raise Exception
        else:
            raise ValueError(f'Unsupported NS_DEF type {NS_DEF}!')
        # update the input
        optimx.step()
        # project the input (L_\infty bound)
        if not unbound:
            if images_orig.min() >= 0. and images_orig.max() <= 1.:
                images = th.min(images, images_orig + eps)
                images = th.max(images, images_orig - eps)
            elif images_orig.min() < 0.:
                images = th.min(images, images_orig + (eps/IMstd[:,None,None]).to(device))
                images = th.max(images, images_orig - (eps/IMstd[:,None,None]).to(device))
            else:
                raise Exception

        if images_orig.min() >= 0. and images_orig.max() <= 1.:
            images = th.clamp(images, min=0., max=1.)
        elif images_orig.min() < 0.:
            images = th.max(images, renorm(th.zeros(images.shape, device=device)))
            images = th.min(images, renorm(th.ones(images.shape, device=device)))
        else:
            raise Exception
        # detach from computation graph and prepare for the next round
        images = images.clone().detach()
        traj.append(images.clone().detach())
        images.requires_grad = True
        if maxiter > 1 and verbose:
            cprint('  (Ski-A)' if _iseven(iteration) else '  (Ski-D)', 'blue', end=' ')
            print(f'iter {iteration:4d}', f'\tloss= {loss.item():7.4f}',
                    f'\tL2m= {(images-images_orig).norm(2,dim=1).mean():7.4f}',
                    f'\tL0m= {(images-images_orig).abs().max(dim=1)[0].mean():7.4f}')

    # flashback stage: Ski-T (this step is effective on Fashion, but not on Cifar10)
    for iteration in range(maxiterT):
        optim = th.optim.SGD(model.parameters(), lr=0)
        optim.zero_grad()
        optimx = th.optim.SGD([images], lr=1.)
        optimx.zero_grad()
        output_T, loss_T = model.loss(images, labels, adv=False)
        loss_T.backward()
        # dispatch attack step
        if NS_DEF == 'PGD':
            if images_orig.min() >= 0. and images_orig.max() <= 1.:
                images.grad.data.copy_(alpha * th.sign(images.grad))
            elif images_orig.min() < 0.:
                images.grad.data.copy_((alpha/IMstd[:,None,None]).to(device) * th.sign(images.grad))
            else:
                raise Exception
        else:
            raise ValueError("unsupported NS_DEF type")
        optimx.step()
        # projection
        if not unbound:
            if images_orig.min() >= 0. and images_orig.max() <= 1.:
                images = th.min(images, images_orig + eps)
                images = th.max(images, images_orig - eps)
            elif images_orig.min() < 0.:
                images = th.min(images, images_orig + (eps/IMstd[:,None,None]).to(device))
                images = th.max(images, images_orig - (eps/IMstd[:,None,None]).to(device))
            else:
                raise Exception
        if images_orig.min() >= 0. and images_orig.max() <= 1.:
            images = th.clamp(images, min=0., max=1.)
        elif images_orig.min() < 0.:
            images = th.max(images, renorm(th.zeros(images.shape, device=device)))
            images = th.min(images, renorm(th.ones(images.shape, device=device)))
        else:
            raise Exception
        # detach and evaluate
        images = images.clone().detach()
        traj.append(images.clone().detach())
        images.requires_grad = True
        if maxiterT > 1 and verbose:
            cprint('  (Ski-T)', 'blue', end=' ')
            print(f'iter {iteration:4d}', f'\tloss= {loss_T.item():7.4f}',
                    f'\tL2m= {(images-images_orig).norm(2,dim=1).mean():7.4f}',
                    f'\tL0m= {(images-images_orig).abs().max(dim=1)[0].mean():7.4f}')

    xr = images  # th.tensor
    r = images - images_orig  # th.tensor
    traj = th.stack(traj) # th.tensor
    if verbose:
        if images_orig.min() >= 0. and images_orig.max() <= 1.:
            tmp = r.view(r.shape[0], -1)
        elif images_orig.min() < 0.:
            tmp = r.mul(IMstd[:,None,None].to(r.device)).view(r.shape[0], -1)
        cprint('r>', 'white', 'on_grey', end=' ')
        print('Min', '%.3f'%tmp.min().item(),
                'Max', '%.3f'%tmp.max().item(),
                'Mean', '%.3f'%tmp.mean().item(),
                'L0', '%.3f'%tmp.norm(0, dim=1).mean().item(),
                'L1', '%.3f'%tmp.norm(1, dim=1).mean().item(),
                'L2', '%.3f'%tmp.norm(2, dim=1).mean().item())
    if verbose:
        # VALIDATION: mean shift
        cprint('Ski>', 'white', 'on_red', end=' ')
        print('L2=', r.view(r.shape[0], -1).norm(2, dim=1).mean().item() , end='\t')
        print('L1=', r.view(r.shape[0], -1).norm(1, dim=1).mean().item())

    # xr.shape   = (Batch * CHW)
    # r.shape    = (Batch * CHW)
    # traj.shape = (numTraj * Batch * CHW)
    return (xr, r, traj)


def NeuroSkiValidate(model, images, labels, *, dconf={}, verbose=True, device='cpu'):
    '''
    Validation experiment for neuroski
    '''
    assert(type(images) == th.Tensor)
    DIMR = PCA # TSNE, Isomap, MDS, LocallyLinearEmbedding, PCA

    # keep a duplicate
    images = images.to(device)
    images_orig = images.clone().detach()
    images.requires_grad = True
    labels = labels.to(device).view(-1)

    # baseline: forward
    model.eval()
    with th.no_grad():
        output, loss = model.loss(images, labels, adv=False)
        orig_correct = output.max(1)[1].eq(labels).sum().item()
        output_orig = output.clone().detach()
        loss_orig = loss.clone().detach()
    if verbose:
        cprint('Orig Classification>', 'green', 'on_white', end=' ')
        print(f'loss= {loss.item():.3f}', f'accuracy= {orig_correct/len(labels):.3f}')

    # start neuroski on benign example + correct/random label
    cprint('>_< NeuroSki Benign Example ...', 'white', 'on_blue')
    xr_b, r_b, traj_b = neuroSki(model, images, labels, eps=dconf['epsilon'],
            alpha=2./255., maxiter=dconf['nsmaxiter'], verbose=verbose,
            device=device, targeted=dconf['targeted'], unbound=dconf['unbound'])

    if False: # inspect benign
        trajx = [x.view(x.shape[0], -1).detach().cpu().numpy() for x in traj_b]
        for ni in range(xr_b.shape[0]):
            tr = np.array([x[ni] for x in trajx])
            tremb = DIMR(n_components=2).fit_transform(tr)
            print('Trajectory shape', tr.shape, 'embedding shape', tremb.shape)
            print(tr.mean(1), tr.max(1), tr.min(1), np.linalg.matrix_rank(tr))
            print(tremb)
            lab.figure()
            lab.plot(tremb[:,0], tremb[:,1], c='gray', marker='')
            lab.scatter(tremb[0,0], tremb[0,1], c='blue')
            lab.scatter(tremb[1:-1,0], tremb[1:-1,1], c='lime')
            lab.scatter(tremb[-1:,0], tremb[-1:,1], c='red')
            lab.show()

    # generate untargeted adversarial exmaples using PGD
    cprint('>_< NeuroSki Adversarial Example ...', 'white', 'on_blue')
    xr_adv, r_adv = projectedGradientDescent(model, images, labels,
            eps=dconf['epsilon'], alpha=2./255., maxiter=dconf['maxiter'],
            verbose=verbose, device=device, targeted=False, unbound=False)
    model.eval()
    with th.no_grad():
        output_adv, loss_adv = model.loss(xr_adv, labels, adv=False)
        pred_adv = output_adv.max(1)[1]
        correct_adv = pred_adv.eq(labels).sum().item()
        if verbose:
            cprint('PGD Classification>', 'green', 'on_white', end=' ')
            print(f'loss= {loss_adv.item():.5f}', f'accuracy= {correct_adv/len(pred_adv):.3f}')

    # start neuroski on adversarial example + pred/random labels
    #print(xr_adv[0].view(-1)[:10]) #debug
    model.eval()
    xr_a, r_a, traj_a = neuroSki(model, xr_adv, pred_adv, eps=dconf['epsilon'],
            alpha=2./255., maxiter=dconf['nsmaxiter'], verbose=verbose,
            device=device, targeted=dconf['targeted'], unbound=dconf['unbound'])

    if False: # inspect adversarial
        trajy = [x.view(x.shape[0], -1).detach().cpu().numpy() for x in traj_a]
        for ni in range(xr_a.shape[0]):
            if pred_adv[ni] == labels[ni]:
                continue
            else:
                print('Orig', labels[ni], 'AdvPred', pred_adv[ni])
            tr = np.array([x[ni] for x in trajy])
            tremb = DIMR(n_components=2).fit_transform(tr)
            print(tr)
            print('Trajectory shape', tr.shape, 'embedding shape', tremb.shape)
            print(tremb)
            lab.figure()
            lab.plot(tremb[:,0], tremb[:,1], c='gray', marker='')
            lab.scatter(tremb[0,0], tremb[0,1], c='blue')
            lab.scatter(tremb[1:-1,0], tremb[1:-1,1], c='lime')
            lab.scatter(tremb[-1:,0], tremb[-1:,1], c='red')
            lab.show()

    # start neuroski on adversarial example + correct/random label
    #print(xr_adv[0].view(-1)[:10]) #debug
    cprint('>_< NeuroSki Adversarial Reset ...', 'white', 'on_blue')
    model.eval()
    xr_r, r_r, traj_r = neuroSki(model, xr_adv, labels, eps=dconf['epsilon'],
            alpha=2./255., maxiter=dconf['nsmaxiter'], verbose=verbose,
            device=device, targeted=dconf['targeted'], unbound=dconf['unbound'])

    if False: # inspect all three trajectories
        # TODO: display the trajectory for more than one sample at a time?
        trajb = [x.view(x.shape[0], -1).detach().cpu().numpy() for x in traj_b]
        traja = [x.view(x.shape[0], -1).detach().cpu().numpy() for x in traj_a]
        trajr = [x.view(x.shape[0], -1).detach().cpu().numpy() for x in traj_r]
        for ni in range(xr_a.shape[0]):
            if pred_adv[ni] == labels[ni]:
                continue
                # note, they have larger Ski distance than adversarial examples
                # TODO: Why? Are these examples abnormal?
                print('!!!!!!!!!! Orig', labels[ni], 'AdvPred', pred_adv[ni])
            else:
                print('Orig', labels[ni], 'AdvPred', pred_adv[ni])
            tremb = DIMR(n_components=2).fit_transform(
                    np.concatenate([
                        np.array([x[ni] for x in trajb]),
                        np.array([x[ni] for x in traja]),
                        np.array([x[ni] for x in trajr]),
                        ], axis=0)
                    )
            print('* Emb Shape', tremb.shape)
            trembb = tremb[:tremb.shape[0]//3]
            tremba = tremb[tremb.shape[0]//3:-tremb.shape[0]//3]
            trembr = tremb[-tremb.shape[0]//3:]
            print(np.linalg.norm(tremba[0]  - trembr[0], 2))
            print('* Benign Ski |', 'L2=', (xr_b[ni] - images_orig[ni]).norm(2).item(),
                    'L1=', (xr_b[ni] - images_orig[ni]).norm(1).item())
            print('* Advers Ski |', 'L2=', (xr_a[ni] - xr_adv[ni]).norm(2).item(),
                    'L1=', (xr_a[ni] - xr_adv[ni]).norm(1).item())
            print('* Reset  Ski |', 'L2=', (xr_r[ni] - xr_adv[ni]).norm(2).item(),
                    'L1=', (xr_r[ni] - xr_adv[ni]).norm(2).item())
            #print(tremb)
            lab.subplot(141)
            lab.plot(trembb[:,0], trembb[:,1], c='blue', marker='', linewidth=0.7)
            lab.scatter(trembb[0,0], trembb[0,1], c='blue')
            lab.scatter(trembb[1:-1,0], trembb[1:-1,1], c='lime')
            lab.scatter(trembb[-1:,0], trembb[-1:,1], c='red')
            lab.subplot(142)
            lab.plot(tremba[:,0], tremba[:,1], c='red', marker='', linewidth=0.7)
            lab.scatter(tremba[0,0], tremba[0,1], c='blue')
            lab.scatter(tremba[1:-1,0], tremba[1:-1,1], c='lime')
            lab.scatter(tremba[-1:,0], tremba[-1:,1], c='red')
            lab.subplot(143)
            lab.plot(trembr[:,0], trembr[:,1], c='lime', marker='', linewidth=0.7)
            lab.scatter(trembr[0,0], trembr[0,1], c='blue')
            lab.scatter(trembr[1:-1,0], trembr[1:-1,1], c='lime')
            lab.scatter(trembr[-1:,0], trembr[-1:,1], c='red')
            lab.subplot(144)
            lab.plot(trembb[:,0], trembb[:,1], c='blue', marker='', linewidth=0.7)
            lab.scatter(trembb[0,0], trembb[0,1], c='blue')
            lab.scatter(trembb[1:-1,0], trembb[1:-1,1], c='lime')
            lab.scatter(trembb[-1:,0], trembb[-1:,1], c='red')
            lab.plot(tremba[:,0], tremba[:,1], c='red', marker='', linewidth=0.7)
            lab.scatter(tremba[0,0], tremba[0,1], c='blue')
            lab.scatter(tremba[1:-1,0], tremba[1:-1,1], c='lime')
            lab.scatter(tremba[-1:,0], tremba[-1:,1], c='red')
            lab.plot(trembr[:,0], trembr[:,1], c='lime', marker='', linewidth=0.7)
            lab.scatter(trembr[0,0], trembr[0,1], c='blue')
            lab.scatter(trembr[1:-1,0], trembr[1:-1,1], c='lime')
            lab.scatter(trembr[-1:,0], trembr[-1:,1], c='red')
            lab.show()

    l2_benign = r_b.view(r_b.size(0), -1).norm(2, dim=1).mean().item()
    l1_benign = r_b.view(r_b.size(0), -1).norm(1, dim=1).mean().item()
    l2_adversarial = r_a.view(r_a.size(0), -1).norm(2, dim=1).mean().item()
    l1_adversarial = r_a.view(r_a.size(0), -1).norm(1, dim=1).mean().item()
    l2_agtb = (r_a.view(r_a.size(0), -1).norm(2, dim=1) >
            r_b.view(r_b.size(0), -1).norm(2, dim=1)).float().mean().item()
    l1_agtb = (r_a.view(r_a.size(0), -1).norm(1, dim=1) >
            r_b.view(r_b.size(0), -1).norm(1, dim=1)).float().mean().item()
    stat = {'l2_benign': l2_benign, 'l1_benign': l1_benign, 'l2_adversarial': l2_adversarial,
            'l1_adversarial': l1_adversarial, 'l2_agtb': l2_agtb, 'l1_agtb': l1_agtb}
    return stat


def neuroSkiTraverse(model, images, labels, *, dconf={}, verbose=False, device='cpu'):
    '''
    Traversal function used for neuroski regression
    '''
    assert(type(images) == th.Tensor)
    # keep a duplicate
    images = images.to(device)
    labels = labels.to(device).view(-1)
    # baseline: forward
    model.eval()
    with th.no_grad():
        output, _ = model.loss(images, labels, adv=False)
    label_upper = output.size(1)
    del output
    xrs, trajs = [], []
    for c in range(label_upper):
        fakelabels = th.ones_like(labels, device=labels.device) * c
        xr_c, r_c, traj_c = neuroSki(model, images, fakelabels, eps=dconf['epsilon'],
                alpha=2./255.,
                maxiter=dconf['nsmaxiter'], verbose=verbose,
                device=device, targeted=dconf['targeted'], unbound=dconf['unbound'],
                maxiterT=0)
        xrs.append(xr_c.clone().detach())
        trajs.append(traj_c)
    # xrs.shape = list_numClass[ Batch * CHW ]
    # trajs.shape = list_numClass[ numTraj * Batch * CHW ]
    return (xrs, trajs)


def NeuroSkiZigRegression(model, images, labels, *, dconf={}, verbose=True,
        device='cpu', vote=False, dash=False):
    '''
    Regression experiment for neuroski
    '''
    assert(type(images) == th.Tensor)
    DIMR = str(os.getenv('NS_DIMR', 'PCA'))
    DIMR = eval(DIMR) # TSNE, Isomap, MDS, LocallyLinearEmbedding, PCA

    if vote: raise NotImplementedError
    if dash: raise NotImplementedError

    # keep a duplicate
    images = images.to(device)
    images_orig = images.clone().detach()
    images.requires_grad = True
    labels = labels.to(device).view(-1)

    # baseline: forward
    model.eval()
    with th.no_grad():
        output, loss = model.loss(images, labels, adv=False)
        label_upper = output.shape[1]
        orig_correct = output.max(1)[1].eq(labels).sum().item()
        acc_orig = orig_correct/len(labels)
        output_orig = output.clone().detach()
        loss_orig = loss.clone().detach()
    if verbose:
        cprint('Orig Classification>', 'green', 'on_white', end=' ')
        print(f'loss= {loss.item():.3f}', f'accuracy= {acc_orig:.3f}')

    # generate untargeted adversarial exmaples using $NS_ATK
    cprint('    >_< Generate Adversarial Example ...', 'white', 'on_grey')
    NS_ATK = os.getenv('NS_ATK', 'N/A')
    if NS_ATK == 'N/A':
        xr_adv, r_adv = images, th.zeros_like(images, device=images.device)
    elif NS_ATK == 'UT:PGD':
        xr_adv, r_adv = projectedGradientDescent(model, images, labels,
                eps=dconf['epsilon'],
                alpha=2./255.,
                maxiter=dconf['maxiter'], verbose=verbose,
                device=device, targeted=False, unbound=False)
    elif NS_ATK == 'UT:FGSM':
        xr_adv, r_adv = projectedGradientDescent(model, images, labels,
                eps=dconf['epsilon'],
                alpha=2./255.,
                maxiter=1, verbose=verbose, # note, maxiter is 1
                device=device, targeted=False, unbound=False)
    else:
        raise ValueError(f'Unsupported attack type NS_ATK={NS_ATK}')
    model.eval()
    with th.no_grad():
        output_adv, loss_adv = model.loss(xr_adv, labels, adv=False)
        pred_adv = output_adv.max(1)[1]
        correct_adv = pred_adv.eq(labels).sum().item()
        acc_adv = correct_adv/len(labels)
        if verbose:
            cprint('PGD Classification>', 'green', 'on_white', end=' ')
            print(f'loss= {loss_adv.item():.5f}', f'accuracy= {correct_adv/len(pred_adv):.3f}')

    # start neuroski regression on adversarial example
    cprint('>_< NeuroSki Regression | Adversarial ...', 'white', 'on_blue')
    model.eval()
    xrsa, trajsa = neuroSkiTraverse(model, xr_adv, labels, dconf=dconf, device=device, verbose=verbose)
    # ( L2 )
    l2dmat_adver = th.stack([(x - xr_adv).view(x.size(0), -1).norm(2, dim=1) for x in xrsa]).t() # Batch x Classes
    nspred_adver = l2dmat_adver.min(dim=1)[1]
    acc_ns_adver = (nspred_adver == labels).float().mean().item()
    acc_ns_adver_max = (l2dmat_adver.max(dim=1)[1] == labels).float().mean().item()
    dom_l2 = ((l2dmat_adver.topk(k=2,dim=1,largest=False)[0][:,1]
              - l2dmat_adver.min(dim=1)[0]) / (l2dmat_adver.max(dim=1)[0] - l2dmat_adver.min(dim=1)[0])).mean().item()
    # ( L2 Ballot for ZREGX ), trajsa.shape: class * numTraj * batch * CHW
    ballot = (th.stack(trajsa) - xr_adv).view(len(trajsa), trajsa[0].shape[0], trajsa[0].shape[1], -1).norm(2, dim=3) # Class x numTraj x Batch
    ballot = ballot.min(dim=0)[1].t() # Batch * numTraj
    zregx_last = (ballot[:,-1] == labels).float().mean().item()
    zregx_evote = (th.tensor([x[::2].bincount().argmax() for x in ballot],
        device=ballot.device) == labels).float().mean().item()
    zregx_enear = (th.tensor([x[::2].bincount(
        th.linspace(0,1,steps=x[::2].shape[0],device=ballot.device)).argmax() for x in ballot],
        device=ballot.device) == labels).float().mean().item()
    print("BALLOT", ballot.shape, ballot, "labels", labels)
    # ( Cos Reset )
    strajsa = th.stack(trajsa)
    incvecs_even = th.nn.functional.normalize((strajsa[:,1:] - strajsa[:,:-1])[:,1::2].view(
        strajsa.shape[0], strajsa.shape[1]//2, strajsa.shape[2], -1), p=2, dim=3) # class * numTraj // 2 * batch * -1(CHW)
    incvecs_even = incvecs_even.transpose(1,2).transpose(0,1)
    cosreset = th.matmul(incvecs_even, incvecs_even.transpose(2,3)) # batch x class x traj//2 x traj//2
    cosreset = cosreset.view(cosreset.shape[0], cosreset.shape[1], -1).mean(dim=2) # batch x class
    acc_cos = (cosreset.max(dim=1)[1] == labels).float().mean().item() # max correlation of reset vectors
    # ( L1 ) 
    l1dmat_adver = th.stack([(x - xr_adv).view(x.size(0), -1).norm(1, dim=1) for x in xrsa]).t() # Batch x Classes
    nspredl1_adver = l1dmat_adver.min(dim=1)[1]
    acc_ns_l1_adver = (nspredl1_adver == labels).float().mean().item()
    acc_ns_l1_adver_max = (l1dmat_adver.max(dim=1)[1] == labels).float().mean().item()
    if verbose:
        print('NSReg| min.hit:', acc_ns_adver, 'max.hit', acc_ns_adver_max, 'shape=', l2dmat_adver.shape)
    
    if bool(os.getenv('NS_VIS_FRAC', False)): # inspect all the trajectories
        # visualize trajsb and trajsa, shape: cls * traj * batchsize * image
        for ni in range(len(images)):
            # let's draw the figure
            lab.figure()
            lab.grid(True)

            # [[ fig1: adversarial ]]
            lab.subplot(131)
            trsa = th.stack([trajsa[j][:,ni,:,:,:] for j in range(label_upper)])
            trsa = trsa.view(trsa.size(0), trsa.size(1), -1) # cls, traj, flatten
            esa = DIMR(n_components=2).fit_transform(trsa.view(-1, trsa.size(-1)).cpu().numpy())
            for j in range(label_upper):
                # draw start point
                lab.scatter(esa[j*numtraj, 0], esa[j*numtraj, 1], c='blue')
                # draw trajectory and endpoint
                if j == labels[ni].item():
                    lab.plot(esa[j*numtraj:(j+1)*numtraj, 0], esa[j*numtraj:(j+1)*numtraj, 1], c='red', marker='', linewidth=0.8)
                    lab.scatter(esa[(j+1)*numtraj-1, 0], esa[(j+1)*numtraj-1, 1], c='red') # red
                else:
                    lab.plot(esa[j*numtraj:(j+1)*numtraj, 0], esa[j*numtraj:(j+1)*numtraj, 1], c='magenta', marker='', linewidth=0.5)
                    lab.scatter(esa[(j+1)*numtraj-1, 0], esa[(j+1)*numtraj-1, 1], c='lime') # lime: wrong reset
            lab.title(f'GT: {labels[ni].item()} ADV: {pred_adv[ni].item()} MIN: {nspred_adver[ni].item()}')

            # [[ show them all! ]]
            lab.show() # the GUI blocks

    if bool(os.getenv('NS_VIS_TRAJ', False)):
        # visualize the trajectory
        # first transform (cls * numtraj * batch * chw) into (batch, cls, numtraj, chw)
        tmp = strajsa.cpu().transpose(1, 2).transpose(0, 1)
        for ni in range(len(images)):
            lab.figure()
            numcls, numtraj = tmp.shape[1], tmp.shape[2]
            for i in range(numcls):
                for j in range(numtraj):
                    lab.subplot(numcls, numtraj, 1 + i * numtraj + j)
                    if j == 0:
                        lab.title('Ski ' + str(i))
                    else:
                        #lab.title('%.2f' % (tmp[ni, i, j] - tmp[ni, i, 0]).norm(2).item())
                        lab.title('%.2f' % (tmp[ni, i, j] - xr_adv[ni].to(tmp.device)).norm(2).item())
                    im = tmp[ni, i, j].squeeze().numpy()
                    lab.imshow(im, cmap='gray')
                    lab.axis('off')
                    print('.', end='') #! row', i, 'col', j, im.shape, im.max(), im.min())
                    sys.stdout.flush()
            print()
            print('Orig cls', labels[ni].item(), 'Adv cls', pred_adv[ni].item())
            lab.show()

    stat = {'acc_orig': acc_orig,
            'acc_adv': acc_adv,
            'acc_ns_adver': acc_ns_adver,
            'acc_ns_adver_max': acc_ns_adver_max,
            'acc_ns_l1_adver': acc_ns_l1_adver,
            'acc_ns_l1_adver_max': acc_ns_l1_adver_max,
            'dom_l2': dom_l2,
            'zregx_last': zregx_last,
            'zregx_evote': zregx_evote,
            'zregx_enear': zregx_enear,
            'acc_cos': acc_cos,
            }
    return stat
