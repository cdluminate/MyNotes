'''
ResNet for Image Classification on ImageNet
Reference: https://github.com/pytorch/examples/blob/master/imagenet/main.py

GPU mem usage: Xeon E5-2687Wv4 @TitanX Pascal *1 -- Pytorch 1.0.0
  Resnet18: 8800Mib (batch=256)
'''
import os
import sys
import argparse

import torch as th
import torchvision as vision
from tqdm import tqdm


def metric_accuracy(output, labels, topk=(1,5)):
    with th.no_grad():
        batchsize = labels.size(0)
        _, pred = output.topk(max(topk), 1, True, True)
        pred = pred.t()
        correct = pred.eq(labels.view(1, -1).expand_as(pred))
        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batchsize))
        res = [x.item() for x in res]
        return res


def adjustLr(optim, lr):
    '''
    Adjust learning rate for a given optimizer.
    '''
    for param_group in optim.param_groups:
        param_group['lr'] = lr


def validate(model, valloader, crit):
    '''
    Validate model on the given validation dataset
    '''
    return  #FIXME
    model.eval()
    with th.no_grad():
        for iteration, (images, labels) in tqdm(enumerate(valloader), total=len(valloader)):
            images = images.to(ag.device)
            labels = labels.to(ag.device)

            # forward pass
            output = model(images)
            loss = crit(output, labels)
            accuracy = metric_accuracy(output, labels)
            print(f'Validation:', f'loss {loss:.3f}', f'Acc@1 {accuracy[0]:.1f}%', f'Acc@5 {accuracy[1]:.1f}%')


def mainTrain(argv):
    '''
    Train a CNN on imagenet
    '''
    ag = argparse.ArgumentParser()
    ag.add_argument('-D', '--device', default='cpu')
    ag.add_argument('--pool', type=str, required=True)
    ag.add_argument('--cnn', type=str, default='resnet18')
    ag.add_argument('--lr', type=float, default=1e-1)
    ag.add_argument('--batch', type=int, default=256)
    ag.add_argument('--maxepoch', type=int, default=90)
    ag.add_argument('--reportevery', type=int, default=10)
    ag = ag.parse_args(argv)
    ag.device = th.device(ag.device)

    # Load dataset
    print('* Loading dataset ...', end=' ')
    normalize = vision.transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225])
    trainset = vision.datasets.ImageFolder(
            os.path.join(ag.pool, 'train'),
            vision.transforms.Compose([
                vision.transforms.RandomResizedCrop(224),
                vision.transforms.RandomHorizontalFlip(),
                vision.transforms.ToTensor(),
                normalize,
            ]))
    #valset = vision.datasets.ImageFolder(
    #        os.path.join(ag.pool, 'val'),
    #        vision.transforms.Compose([
    #            vision.transforms.Resize(256),
    #            vision.transforms.CenterCrop(224),
    #            vision.transforms.ToTensor(),
    #            normalize,
    #        ]))
    print('OK')
    trainloader = th.utils.data.DataLoader(
            trainset, batch_size=ag.batch, shuffle=True, num_workers=4, pin_memory=True)
    #valloader = th.utils.data.DataLoader(
    #        valset, batch_size=ag.batch, shuffle=False, num_workers=4, pin_memory=True)
    print(f'Training set size', len(trainset))
    #print(f'Validation set size', len(valset))

    # Create CNN, criterion and optimizer
    model = getattr(vision.models, ag.cnn)().to(ag.device)
    crit = th.nn.CrossEntropyLoss().to(ag.device)
    optim = th.optim.SGD(model.parameters(), lr=ag.lr, momentum=0.9, weight_decay=1e-4)
    print(model)

    # Start training
    #validate(model, valloader, crit)
    for epoch in range(ag.maxepoch):
        model.train()

        # adjust learning rate
        lr = ag.lr * (0.1 ** (epoch // 30))
        adjustLr(optim, lr)

        for iteration, (images, labels) in enumerate(trainloader):
            images = images.to(ag.device)
            labels = labels.to(ag.device)

            # forward pass
            output = model(images)
            loss = crit(output, labels)
            accuracy = metric_accuracy(output, labels)
            if 0 == iteration % ag.reportevery:
                print(f'Eph[{epoch}][{iteration}/{len(trainloader)}]',
                        f'loss {loss:.3f}',
                        f'Acc@1 {accuracy[0]:.1f}%',
                        f'Acc@5 {accuracy[1]:.1f}%')

            # backward pass
            optim.zero_grad()
            loss.backward()
            optim.step()

        # validate model after each epoch
        validate(model, valloader, crit)

if __name__ == '__main__':
    print('* Using TH', th.__version__, f'\tCUDA Status: {th.cuda.is_available()}')
    eval(f'main{sys.argv[1]}')(sys.argv[2:])
