'''
https://lightning.ai/docs/pytorch/stable/notebooks/lightning_examples/cifar10-baseline.html

Note, distributed data parallel training can reduce performance.
Benign Training. 2* Nvidia Quadro RTX8000 (48GB)
2GPU  30 eph accuracy 83.7%
2GPU  50 eph accuracy 86.6%
2GPU 100 eph accuracy 87.8%
2GPU 150 eph accuracy 88.7%
1GPU  30 eph accuracy 91.8%
1GPU  50 eph accuracy 92.7%
1GPU 100 eph accuracy 94.2%
'''
import os
# disabling NCCL's nvlink communication is necessary on many servers.
os.putenv('NCCL_P2P_DISABLE', '1')
import torch as th
import torch.nn.functional as F
import torchvision as V
from pl_bolts.datamodules import CIFAR10DataModule
from pl_bolts.transforms.dataset_normalizations import cifar10_normalization
from pytorch_lightning import LightningModule, Trainer, seed_everything
from pytorch_lightning.callbacks import LearningRateMonitor
from pytorch_lightning.callbacks.progress import TQDMProgressBar
from pytorch_lightning.loggers import CSVLogger, TensorBoardLogger
from torch.optim.lr_scheduler import OneCycleLR
from torch.optim.swa_utils import AveragedModel, update_bn
from torchmetrics.functional import accuracy
import argparse
import rich
console = rich.get_console()



train_transforms = V.transforms.Compose([
    V.transforms.RandomCrop(32, padding=4),
    V.transforms.RandomHorizontalFlip(),
    V.transforms.ToTensor(),
    ])

test_transforms = V.transforms.Compose([
    V.transforms.ToTensor(),
    ])


def create_dataset(args):
    cifar10_dm = CIFAR10DataModule(
            data_dir=args.datadir,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            train_transforms=train_transforms,
            test_transforms=test_transforms,
            val_transforms=test_transforms,
            )
    return cifar10_dm


def create_model(args):
    model = V.models.resnet18(pretrained=False, num_classes=10)
    model.conv1 = th.nn.Conv2d(3, 64, kernel_size=(3,3), stride=(1,1),
                               padding=(1,1), bias=False)
    model.maxpool = th.nn.Identity()
    return model


class LitResNet(LightningModule):
    def __init__(self, args):
        super().__init__()
        self.model = create_model(args)
        self.args = args
    def forward(self, x):
        x = cifar10_normalization()(x)
        out = self.model(x)
        return out
    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        self.log('train_loss', loss)
        return loss
    def evaluate(self, batch, stage=None):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        preds = th.argmax(logits, dim=1)
        acc = accuracy(preds, y, task='multiclass', num_classes=10, top_k=1)
        if stage:
            self.log(f'{stage}_loss', loss, prog_bar=True)
            self.log(f'{stage}_acc', acc, prog_bar=True)
    def validation_step(self, batch, batch_idx):
        self.evaluate(batch, 'val')
    def test_step(self, batch, batch_idx):
        self.evaluate(batch, 'val')
    def configure_optimizers(self):
        optimizer = th.optim.SGD(
                self.parameters(),
                lr=self.args.lr,
                momentum=0.9,
                weight_decay=5e-4,
                )
        steps_per_epoch = 45000 // self.args.batch_size
        scheduler_dict = {
                'scheduler': OneCycleLR(optimizer,
                                        self.args.lr_max,
                                        epochs=self.trainer.max_epochs,
                                        steps_per_epoch=steps_per_epoch),
                'interval': 'step',
                }
        return {'optimizer': optimizer, 'lr_scheduler': scheduler_dict}


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--device', '-d', type=str,
                    default='cuda' if th.cuda.is_available() else 'cpu')
    ag.add_argument('--batch_size', '-b', type=int, default=256)
    ag.add_argument('--num_workers', '-j', type=int, default=int(os.cpu_count()/2))
    ag.add_argument('--datadir', type=str, default='./data/')
    ag.add_argument('--lr', type=float, default=0.05)
    ag.add_argument('--lr_max', type=float, default=0.1)
    ag.add_argument('--max_epochs', type=int, default=30)
    ag.add_argument('--logdir', type=str, default='logs')
    ag.add_argument('--logger', type=str, default='TensorBoardLogger',
                    choices=('TensorBoardLogger', 'CSVLogger'))
    ag = ag.parse_args()
    console.print(ag)

    cifar10_dm = create_dataset(ag)
    model = LitResNet(ag)
    trainer = Trainer(
            max_epochs=ag.max_epochs,
            accelerator='gpu',
            strategy='ddp',
            devices=th.cuda.device_count() if th.cuda.is_available() else None,
            logger=eval(ag.logger)(save_dir=ag.logdir),
            callbacks=[LearningRateMonitor(logging_interval='step'),
                       TQDMProgressBar(refresh_rate=10)],
            )
    trainer.fit(model, cifar10_dm)
    trainer.test(model, datamodule=cifar10_dm)
