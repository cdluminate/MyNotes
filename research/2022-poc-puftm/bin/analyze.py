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


def analyze(sd, fc2) -> th.Tensor:
    w = sd['fc3.weight']
    print('w', w.shape)
    print('fc2.feats', fc2.shape, fc2.mean(), fc2.std())

    # direct feature visualize
    #plt.pcolormesh(fc2)
    #plt.show()

    # activation ratio by dimension
    actrat = (fc2 > 0.0).float().mean(dim=0).view(-1).numpy()
    #plt.bar(th.arange(len(actrat)), actrat)
    #plt.show()

    # null space of w
    ns = null_space(w.numpy()).astype(float)
    print(ns.shape)  # 84x..
    print(ns)
    print('null space sanity')
    lincomb = np.random.rand(ns.shape[1]).astype(float)
    bz = (ns @ lincomb).astype(np.float32)
    bz = th.from_numpy(bz) * 100
    print('bz', bz.shape)
    print(bz @ w.T)
    x1 = fc2 @ w.T
    print(fc2.dtype, bz.dtype, w.dtype)
    x2 = (fc2 + bz) @ w.T
    diff = x1 - x2
    print('diff > 1e-4', (diff > 1e-4).sum())

    if False: # method 1
        # least square
        print('[pre] ls', ns.shape, actrat.shape)
        ls = lstsq(ns, actrat * 100)
        #print('ls', ls)
        sol = ls[0]
        print('ls-sol', sol.shape)

    if True: # method 2
        ls = lstsq(ns, (actrat > 0.5).astype(float) * 100)
        sol = ls[0]

    # calculate bz
    solbz = ns @ sol
    print('solbz', solbz.shape)
    plt.stem(solbz)
    plt.bar(np.arange(len(actrat)), actrat, color='red')
    plt.show()
    return th.from_numpy(solbz)


def append_and_dump(state_dict, bz, dump):
    console.print(f'editing state_dict -- dump to {dump}')
    assert state_dict['fc2.bias'].shape == bz.shape
    state_dict['fc2.bias'] += bz
    th.save(state_dict, dump)


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--fc2', '-f', type=str,
            default='exps/mnist_lenet/fc2.pt')
    ag.add_argument('--state_dict', '-s', type=str,
            default='exps/mnist_lenet/model_latest.pt')
    ag.add_argument('--new_state_dict', type=str,
            default='exps/mnist_lenet/model_modified.pt')
    ag = ag.parse_args()

    sd = th.load(ag.state_dict, map_location='cpu')
    fc2 = th.load(ag.fc2, map_location='cpu')
    bz = analyze(sd, fc2)
    append_and_dump(sd, bz, ag.new_state_dict)
