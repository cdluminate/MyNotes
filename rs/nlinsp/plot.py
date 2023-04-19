import matplotlib.pyplot as plt
import numpy as np
import json
import argparse
import rich
console = rich.get_console()

if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--json', '-J', type=str)
    ag = ag.parse_args()
    console.print(ag)

    # load data
    with open(ag.json, 'rt') as f:
        d = json.load(f)
    console.print(f'found {len(d)} entries.')
    alpha = [v[0] for (k, v) in d.items()]
    sigma = [v[1] for (k, v) in d.items()]
    top1  = [v[2] for (k, v) in d.items()]
    size  = [v[3] for (k, v) in d.items()]
    csize  = np.array(size)
    csize = csize / csize.max()
    
    plt.figure()
    ax1 = plt.subplot(1, 2, 1)
    ax1.scatter(alpha, top1, c=csize, cmap='jet')
    ax1.set_title('alpha vs top1')

    ax2 = plt.subplot(1, 2, 2)
    ax2.scatter(sigma, top1, c=csize, cmap='jet')
    ax2.set_title('sigma vs top1')
    ax2.set_xscale('log')

    plt.show()
