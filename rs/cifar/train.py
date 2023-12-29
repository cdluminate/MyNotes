'''
https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html
https://lightning.ai/docs/pytorch/stable/notebooks/lightning_examples/cifar10-baseline.html
DDP training usually leads to worse performance on CIFAR.
1. --max_epochs=100 accuracy 94.7
2. --max_epochs=50  accuracy 94.0
3. --max_epochs=30  accuracy 93.0 (default)
'''
import os
import argparse
import torch as th
import torchvision as V
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import rich
from rich.progress import track
console = rich.get_console()


def get_transforms(split: str):
    if split == 'train':
        return V.transforms.Compose([
            V.transforms.RandomCrop(32, padding=4),
            V.transforms.RandomHorizontalFlip(),
            V.transforms.ToTensor(),
            V.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ])
    elif split == 'test':
        return V.transforms.Compose([
            V.transforms.ToTensor(),
            V.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ])
    else:
        raise ValueError(split)


def get_datasets(args):
    trainset = V.datasets.CIFAR10(root=args.data_dir, train=True,
                                  download=True,
                                  transform=get_transforms('train'))
    testset = V.datasets.CIFAR10(root=args.data_dir, train=False,
                                 download=True,
                                 transform=get_transforms('test'))
    return trainset, testset


def get_loaders(args):
    trainset, testset = get_datasets(args)
    trainloader = th.utils.data.DataLoader(trainset, batch_size=args.batch_size,
                                              shuffle=True, num_workers=args.num_workers)
    testloader = th.utils.data.DataLoader(testset, batch_size=args.batch_size,
                                             shuffle=False, num_workers=args.num_workers)
    return trainloader, testloader


def get_model(args):
    if args.arch == 'resnet18':
        model = V.models.resnet18(num_classes=10)
        model.conv1 = th.nn.Conv2d(3, 64, kernel_size=(3,3), stride=(1,1),
                                   padding=(1,1), bias=False)
        model.maxpool = th.nn.Identity()
        return model
    else:
        raise NotImplementedError


def train(args, model, optim, sched, loader, epoch):
    model.train()
    for i, batch in track(enumerate(loader), total=len(loader), description='Train'):
        image, label = batch
        image = image.to(args.device)
        label = label.to(args.device)
        outputs = model(image)
        loss = F.cross_entropy(outputs, label)
        _, pred = outputs.max(dim=-1)
        accuracy = (pred.view(-1) == label.view(-1)).sum() / label.size(0)
        optim.zero_grad()
        loss.backward()
        optim.step()
        sched.step()
        if i % args.report_every == 0:
            console.print(f'Trn[{epoch}][{i+1:3d}/{len(loader)}]',
                          f'lr: {sched.get_last_lr()[0]}',
                          f'loss: {loss.item():.3f}',
                          f'accuracy: {accuracy*100:.1f} (/100)')


@th.no_grad()
def evaluate(args, model, optim, sched, loader, epoch):
    model.eval()
    total_loss = 0
    total = 0
    correct = 0
    for i, batch in track(enumerate(loader), total=len(loader), description='Eval'):
        image, label = batch
        image = image.to(args.device)
        label = label.to(args.device)
        outputs = model(image)
        loss = F.cross_entropy(outputs, label)
        _, pred = outputs.max(dim=-1)
        accuracy = (pred.view(-1) == label.view(-1)).sum() / label.size(0)
        correct += (pred.view(-1) == label.view(-1)).sum()
        total += label.size(0)
        total_loss += loss.item() * label.size(0)
        #if i % args.report_every == 0:
        #    console.print(f'Val[{epoch}][{i+1:3d}/{len(loader)}]',
        #                  f'loss: {loss.item():.3f}',
        #                  f'accuracy: {accuracy*100:.1f} (/100)')
    loss = total_loss / total
    accuracy = correct / total
    console.print(f'Eval[{epoch}]',
                  f'loss: {loss:.3f}',
                  f'accuracy: {accuracy*100:.1f} (/100)')


def save_checkpoint(ckname, args, model, optim, sched, epoch):
    checkpoint = {'model': model.state_dict(), 'optimizer': optim.state_dict(), 'lr_scheduler': sched.state_dict(), 'epoch': epoch, 'args': args}
    th.save(checkpoint, os.path.join(args.log_dir, ckname))



if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--arch', type=str, default='resnet18')
    ag.add_argument('--device', '-d', type=str,
                    default='cuda' if th.cuda.is_available() else 'cpu')
    ag.add_argument('--batch_size', type=int, default=256)
    ag.add_argument('--data_dir', type=str, default='./data')
    ag.add_argument('--num_workers', '-j', type=int, default=4)
    ag.add_argument('--lr', type=float, default=0.05)
    ag.add_argument('--lr_max', type=float, default=0.1)
    ag.add_argument('--weight_decay', type=float, default=5e-4)
    ag.add_argument('--max_epochs', type=int, default=30)
    ag.add_argument('--start_epoch', type=int, default=0)
    ag.add_argument('--log_dir', type=str, default='example')
    ag.add_argument('--amp', action='store_true')
    ag.add_argument('--report_every', type=int, default=30)
    ag.add_argument('--resume', type=str, default='')
    ag.add_argument('--eval', action='store_true')
    ag = ag.parse_args()
    console.print(ag)
    if not os.path.exists(ag.log_dir):
        os.mkdir(ag.log_dir)

    console.print('>_< Loading datasets ...')
    trainloader, testloader = get_loaders(ag)

    console.print('>_< Initialize model and optimizer ...')
    model = get_model(ag).to(ag.device)
    optim = th.optim.SGD(model.parameters(), lr=ag.lr, momentum=0.9, weight_decay=ag.weight_decay)
    sched = th.optim.lr_scheduler.OneCycleLR(optim, max_lr=ag.lr_max,
            steps_per_epoch=len(trainloader), epochs=ag.max_epochs)

    if ag.resume:
        ckpt = th.load(ag.resume, map_location=ag.device)
        model.load_state_dict(ckpt['model'])
        optim.load_state_dict(ckpt['optimizer'])
        sched.load_state_dict(ckpt['lr_scheduler'])
        if ag.start_epoch == 0:
            ag.start_epoch = ckpt['epoch']

    if ag.eval:
        evaluate(ag, model, optim, sched, testloader, ckpt['epoch'])
        exit()

    for epoch in range(ag.start_epoch, ag.max_epochs):
        train(ag, model, optim, sched, trainloader, epoch)
        evaluate(ag, model, optim, sched, testloader, epoch)

    console.print('>_< Finished Training')
    save_checkpoint('latest.pth', ag, model, optim, sched, epoch)
