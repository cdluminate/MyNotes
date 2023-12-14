'''
https://huggingface.co/docs/diffusers/tutorials/basic_training
'''
import os
import sys
import numpy as np
import torch as th
import rich
console = rich.get_console()
from datasets import load_dataset
import argparse
import matplotlib.pyplot as plt
import torchvision as V
from diffusers import UNet2DModel, DDPMScheduler, DDPMPipeline
from PIL import Image
import torch.nn.functional as F
from diffusers.optimization import get_cosine_schedule_with_warmup
from diffusers.utils import make_image_grid
from accelerate import Accelerator
from rich.progress import track
import os


def get_transform_fn(config):
    preprocess = V.transforms.Compose([
        V.transforms.Resize((config.image_size, config.image_size)),
        V.transforms.RandomHorizontalFlip(),
        V.transforms.ToTensor(),
        V.transforms.Normalize([0.5], [0.5]),
        ])
    return lambda images: {'images': [preprocess(image.convert('RGB')) for image in images['image']]}


def create_model(config):
    model = UNet2DModel(
            sample_size=config.image_size,
            in_channels=3,
            out_channels=3,
            layers_per_block=2,
            block_out_channels=(128, 128, 256, 256, 512, 512),
            down_block_types=(
                'DownBlock2D', 'DownBlock2D', 'DownBlock2D', 'DownBlock2D',
                'AttnDownBlock2D', 'DownBlock2D',),
            up_block_types=(
                'UpBlock2D', 'AttnUpBlock2D',
                'UpBlock2D', 'UpBlock2D', 'UpBlock2D', 'UpBlock2D',),
            )
    return model


def evaluate(config, epoch, pipeline, accelerator=None):
    images = pipeline(batch_size=config.eval_batch_size,
                      generator=th.manual_seed(config.seed)).images
    image_grid = make_image_grid(images, rows=4, cols=4)
    fpath = os.path.join(config.output_dir, f'epoch-{epoch:04d}.png')
    image_grid.save(fpath)
    console.print('    eval results saved as', fpath)
    if accelerator is not None:
        accelerator.log({'val/visualize-epoch': image_grid}, step=epoch)


def train(config, model, noise_scheduler, optimizer, train_dataloader, lr_scheduler):
    accelerator = Accelerator(
            mixed_precision=config.mixed_precision,
            gradient_accumulation_steps=config.gradient_accumulation_steps,
            log_with='tensorboard',
            project_dir=os.path.join(config.output_dir, 'logs'),
            )
    if accelerator.is_main_process:
        accelerator.init_trackers('train_example')
    model, optimizer, train_dataloader, lr_scheduler = accelerator.prepare(
            model, optimizer, train_dataloader, lr_scheduler)
    global_step = 0
    # start training
    for epoch in range(config.num_epochs):
        # train for one epoch
        if th.distributed.get_rank() == 0:
            iterator = track(enumerate(train_dataloader), total=len(train_dataloader),
                             description=f'Train[{epoch:02d}/{config.num_epochs}]')
        else:
            iterator = enumerate(train_dataloader)
        for step, batch in iterator:
            clean_images = batch['images']
            noise = th.randn(clean_images.shape, device=clean_images.device)
            bs = clean_images.shape[0]
            # sample random timestep for each image
            timesteps = th.randint(
                    0, noise_scheduler.config.num_train_timesteps,
                    (bs,), device=clean_images.device, dtype=th.int64)
            # add noise to images
            noisy_images = noise_scheduler.add_noise(clean_images, noise, timesteps)
            with accelerator.accumulate(model):
                noise_pred = model(noisy_images, timesteps, return_dict=False)[0]
                loss = F.mse_loss(noise_pred, noise)
                accelerator.backward(loss)
                accelerator.clip_grad_norm_(model.parameters(),  1.0)
                optimizer.step()
                lr_scheduler.step()
                optimizer.zero_grad()
            logs = {'trn/loss': loss.detach().item(),
                    'trn/lr': lr_scheduler.get_last_lr()[0],
                    'trn/step': global_step,
                    'trn/epoch': epoch,}
            accelerator.log(logs, step=global_step)
            global_step += 1
        # eval after one epoch
        if accelerator.is_main_process:
            pipeline = DDPMPipeline(unet=accelerator.unwrap_model(model),
                                    scheduler=noise_scheduler)
            if (epoch + 1) % config.save_image_epochs == 0 \
                    or epoch == config.num_epochs - 1:
                evaluate(config, epoch, pipeline, accelerator=accelerator)
            if (epoch + 1) % config.save_model_epochs == 0 \
                    or epoch == config.num_epochs - 1:
                pipeline.save_pretrained(config.output_dir)


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--output_dir', '-o', type=str, default='noise-train')
    ag.add_argument('--train_batch_size', type=int, default=16)
    ag.add_argument('--eval_batch_size', type=int, default=16)
    ag.add_argument('--image_size', type=int, default=128)
    ag.add_argument('--num_epochs', type=int, default=50)
    ag.add_argument('--gradient_accumulation_steps', type=int, default=1)
    ag.add_argument('--learning_rate', type=float, default=1e-4)
    ag.add_argument('--lr_warmup_steps', type=int, default=500)
    ag.add_argument('--save_image_epochs', type=int, default=10)
    ag.add_argument('--save_model_epochs', type=int, default=10)
    ag.add_argument('--mixed_precision', type=str, default='fp16')
    ag.add_argument('--seed', '-S', type=int, default=0)
    ag.add_argument('--dataset_name', type=str,
                    default="huggan/smithsonian_butterflies_subset")
    ag.add_argument('--num_workers', '-j', type=int, default=8)
    ag = ag.parse_args()
    console.print(ag)
    if not os.path.exists(ag.output_dir):
        os.mkdir(ag.output_dir)

    console.print('>_< loading dataset')
    dataset = load_dataset(ag.dataset_name, split='train')
    console.print('    size', len(dataset))

    #demo_fig = os.path.join(ag.output_dir, 'training-vis.png')
    #if not os.path.exists(demo_fig):
    #    console.print('>_< dump training set vis')
    #    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    #    for i, image in enumerate(dataset[:4]['image']):
    #        axs[i].imshow(image)
    #        axs[i].set_axis_off()
    #    plt.savefig(demo_fig)

    console.print('>_< setup transform and dataset')
    dataset.set_transform(get_transform_fn(ag))
    train_dataloader = th.utils.data.DataLoader(dataset,
        batch_size=ag.train_batch_size, shuffle=True, num_workers=ag.num_workers)
    #sample_image = dataset[0]['images'].unsqueeze(0)
    #assert sample_image.shape == (1, 3, 128, 128)

    console.print('>_< setup model')
    model = create_model(ag)
    #assert model(sample_image, timestep=0).sample.shape == (1, 3, 128, 128)

    console.print('>_< setup noise scheduler')
    noise_scheduler = DDPMScheduler(num_train_timesteps=1000)
    #noise = th.randn(sample_image.shape)
    #timesteps = th.LongTensor([50])
    #noisy_image = noise_scheduler.add_noise(sample_image, noise, timesteps)
    #assert noisy_image.shape == (1, 3, 128, 128)
    #noisy_image_pil = Image.fromarray(
    #        ((noisy_image.permute(0, 2, 3, 1) + 1.0) * 127.5).type(th.uint8).cpu().numpy()[0])
    #plt.figure()
    #plt.imshow(noisy_image_pil)
    #plt.savefig(os.path.join(ag.output_dir, 'noisy_image.png'))
    #console.print('>_< MSE loss')
    #noise_pred = model(noisy_image, timesteps).sample
    #loss = F.mse_loss(noise_pred, noise)
    #print(loss.item())
    #del noise_pred
    #del sample_image
    #del noise
    #del timesteps
    #del noisy_image
    #del noisy_image_pil

    console.print('>_< optimizer')
    optimizer = th.optim.AdamW(model.parameters(), lr=ag.learning_rate)
    lr_scheduler = get_cosine_schedule_with_warmup(
            optimizer=optimizer, num_warmup_steps=ag.lr_warmup_steps,
            num_training_steps=(len(train_dataloader) * ag.num_epochs))

    console.print('>_< Start Training ...')
    train(ag, model, noise_scheduler, optimizer, train_dataloader, lr_scheduler)
