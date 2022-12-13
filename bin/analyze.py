'''
POC WIP
'''
import numpy as np
import torch as th
import argparse
import matplotlib.pyplot as plt
from scipy.linalg import null_space, lstsq
import rich
console = rich.get_console()


def puftm(weight_current, feats_previous, *,
        method:str='2', visualize:bool=False) -> th.Tensor:
    '''
    weight_current: shape (output_dimension, input_dimension)
    feats_previous: shape (dataset_size, feature_dimension)
    return: bias vector `bz` 
    '''
    arat = (feats_previous > 0.0).float().mean(dim=0).view(-1).numpy()
    # null space of w
    ns = null_space(weight_current.numpy()).astype(float)
    # solve
    if method == '1':
        ls = lstsq(ns, arat * 10)
        sol = ls[0]
    elif method == '2':
        arat_q = (arat > 0.5).astype(float)
        ls = lstsq(ns, arat_q * 10)
        sol = ls[0]
    elif method == '3':
        raise NotImplementedError
    else:
        raise NotImplementedError
    # calculate solbz
    bz = th.from_numpy(ns @ sol).to(th.float32)
    print('sol: bz', bz.shape)
    if visualize:
        plt.stem(bz)
        plt.bar(np.arange(len(arat)), arat, color='red')
        plt.show()
    # sanity report
    x1 = feats_previous.relu() @ weight_current.T
    x2 = (feats_previous + bz.view(1, -1)).relu() @ weight_current.T
    diff = x2 - x1
    print('diff > 1%:', (diff > x1.mean()/100).sum() / diff.nelement())
    return bz



#def analyze(sd, fc2) -> th.Tensor:
#    w = sd['fc3.weight']
#    print('w', w.shape)
#    print('fc2.feats', fc2.shape, fc2.mean(), fc2.std())
#
#    # direct feature visualize
#    #plt.pcolormesh(fc2)
#    #plt.show()
#
#    # activation ratio by dimension
#    actrat = (fc2 > 0.0).float().mean(dim=0).view(-1).numpy()
#    #plt.bar(th.arange(len(actrat)), actrat)
#    #plt.show()
#
#    # null space of w
#    ns = null_space(w.numpy()).astype(float)
#    print(ns.shape)  # 84x..
#    print(ns)
#    print('null space sanity')
#    lincomb = np.random.rand(ns.shape[1]).astype(float)
#    bz = (ns @ lincomb).astype(np.float32)
#    bz = th.from_numpy(bz) * 100
#    print('bz', bz.shape)
#    print(bz @ w.T)
#    x1 = fc2 @ w.T
#    print(fc2.dtype, bz.dtype, w.dtype)
#    x2 = (fc2 + bz) @ w.T
#    diff = x1 - x2
#    print('diff > 1e-4', (diff > 1e-4).sum())
#
#    if False: # method 1
#        # least square
#        print('[pre] ls', ns.shape, actrat.shape)
#        ls = lstsq(ns, actrat * 100)
#        #print('ls', ls)
#        sol = ls[0]
#        print('ls-sol', sol.shape)
#
#    if True: # method 2
#        ls = lstsq(ns, (actrat > 0.5).astype(float) * 100)
#        sol = ls[0]
#
#    # calculate bz
#    solbz = ns @ sol
#    print('solbz', solbz.shape)
#    plt.stem(solbz)
#    plt.bar(np.arange(len(actrat)), actrat, color='red')
#    plt.show()
#    return th.from_numpy(solbz)



if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--extract', '-e', type=str,
            default='exps/mnist_lenet/extract.pt')
    ag.add_argument('--state_dict', '-s', type=str,
            default='exps/mnist_lenet/model_latest.pt')
    ag.add_argument('--new_state_dict', type=str,
            default='exps/mnist_lenet/model_modified.pt')
    ag.add_argument('--current', type=str, default='fc2,fc3')
    ag.add_argument('--visualize', '-v', action='store_true')
    ag = ag.parse_args()

    # solve and edit
    state_dict = th.load(ag.state_dict, map_location='cpu')
    extract = th.load(ag.extract, map_location='cpu')
    for layername in ag.current.split(','):
        print('processing ...', layername)
        feats_prev = {'fc2': extract['fc1'],
                      'fc3': extract['fc2'],}[layername]
        weight_current = {'fc2': state_dict['fc2.weight'],
                          'fc3': state_dict['fc3.weight'],}[layername]
        bz = puftm(weight_current, feats_prev, visualize=ag.visualize)
        # apply bz
        bias_prev = {'fc2': state_dict['fc1.bias'],
                     'fc3': state_dict['fc2.bias'],}[layername]
        print('before:', 'mean', bias_prev.mean())
        bias_prev += bz
        print('after:', 'mean', bias_prev.mean())
    
    # save and dump
    console.print(f'dump edited state_dict to {ag.new_state_dict}')
    th.save(state_dict, ag.new_state_dict)
