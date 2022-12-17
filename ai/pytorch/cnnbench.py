import argparse
import time
import torch as th
import torchvision as vision

'''
Reference:
    1. https://pytorch.org/docs/stable/nn.html#torch.nn.DataParallel
    2. https://pytorch.org/docs/stable/notes/cuda.html

Notes:
    1. all tensors must be on devices[0] (DataParallel)
'''

if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.add_argument('-D', '--device', type=str, default='cpu')
    ag.add_argument('-M', '--maxepoch', type=int, default=100)
    ag.add_argument('-B', '--batchsize', type=int, default=128)
    ag.add_argument('--model', type=str, default='vgg19')
    ag.add_argument('--single', default=False, action='store_true')
    ag.add_argument('--forward_only', default=False, action='store_true')
    ag = ag.parse_args()
    ag.device = th.device(ag.device)

    # Initialize Network
    print('=> Initializing Neural Network')
    net = getattr(vision.models, ag.model)(False).to(device=ag.device)
    if not ag.single:
        net = th.nn.DataParallel(net, device_ids=[0,1,2,3])
    print(net)

    if ag.forward_only:
        net.eval()
    else:
        net.train()

    mstime = []
    # Fetch Data
    x = th.rand(ag.batchsize, 3, 224, 224, device=ag.device)
    # Epoches/Iterations
    for i in range(ag.maxepoch):
        tm = time.time()
        # Forward
        y = net(x)
        optim = th.optim.Adam(net.parameters(), lr=1e-3, weight_decay=1e-5)
        loss = y.abs().sum()
        if not ag.forward_only:
            # Backward
            optim.zero_grad()
            loss.backward()
            # Update
            optim.step()
        # Report
        mstime.append(1e3*(time.time() - tm))
        print(f'Eph[{i}] loss', loss.item(), '\t',
                'Mean time elapsed (ms)', sum(mstime)/len(mstime))
