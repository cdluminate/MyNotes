import pgdt
import torch as th
import numpy as np
import pandas as pd
import argparse
import json
import timm
import rich
console = rich.get_console()


def one_model_for_arcv(name: str, ishape: int, nclass: int, nsample: int, device:str):
    model = timm.create_model(name, pretrained=False, num_classes=nclass)
    model.eval()
    model = model.to(device)
    images = th.rand(nsample, 3, ishape, ishape)
    images = images.to(device)
    labels = th.randint(0, nclass, (nsample,))
    labels = labels.to(device)
    traj = pgdt.BIM_l8_T(model, images, labels, verbose=False)
    arcm = pgdt.traj2arcm(model, traj, Nclass=nclass)
    arcm = arcm.mean(axis=0)
    arcv = pgdt.arcm2v(arcm)
    return arcv


def traverse_models_for_arcv(csv: str, nclass: int, nsample: int, device:str):
    results = dict()
    csv = pd.read_csv(csv)
    for idx, entry in csv.iterrows():
        model = entry['model']
        img_size = entry['img_size']
        try:
            arcv = one_model_for_arcv(model, img_size, nclass, nsample, device)
            console.print(f'[{idx+1}/{len(csv)}]>', model, img_size, arcv)
        except RuntimeError:
            console.print(f'[{idx+1}/{len(csv)}]>', model, img_size, '[Skipped]')
            continue
        results[model] = arcv.tolist() + [entry.top1, entry.img_size]
        #break # [for debugging]
    return results
    


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--device', '-D', type=str, default='cuda')
    ag.add_argument('--nclass', type=int, default=10)
    ag.add_argument('--nsample', type=int, default=8)
    ag.add_argument('--csv', type=str, default='results-imagenet.csv')
    ag.add_argument('--json', type=str, default=f'{__file__}.json')
    ag = ag.parse_args()
    console.print(ag)
    
    results = traverse_models_for_arcv(ag.csv, ag.nclass, ag.nsample, ag.device)
    with open(ag.json, 'wt') as f:
        json.dump(results, f)
    console.print(f'Results written into {ag.json}')
