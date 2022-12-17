import torch as th
import torchvision as vision
import pylab as lab
from PIL import Image
import numpy as np


device = th.device('cpu')
label = 501

model = vision.models.resnet18(True).to(device)
crit = th.nn.CrossEntropyLoss().to(device)

x = th.rand(1, 3, 224, 224, requires_grad=True).to(device)
label = th.tensor([label], dtype=th.long)
optim = th.optim.Adam([x], lr=1e-2)

imgvis = x.detach().numpy().squeeze().transpose((1,2,0))
imgvis *= [0.229, 0.224, 0.225]
imgvis += [.485, .456, 0.406]
imgvis = imgvis.clip(min=0., max=1.)
lab.imshow(imgvis)
lab.show()

for i in range(10000):

    optim.zero_grad()
    out = model(x)
    loss = crit(out, label)
    loss.backward()
    optim.step()

    print(i, loss.item(), out.argmax(), sep='\t')

    if i % 100==0 and i != 0:
        imgvis = x.detach().numpy().squeeze().transpose((1,2,0))
        imgvis = imgvis.clip(min=0., max=1.)
        lab.imshow(imgvis)
        lab.show()

    if out.argmax().item() == label:
        break

imgvis = x.detach().numpy().squeeze().transpose((1,2,0))
imgvis = imgvis.clip(min=0., max=1.)
lab.imshow(imgvis)
lab.show()
