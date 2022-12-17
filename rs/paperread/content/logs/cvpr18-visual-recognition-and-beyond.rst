---
title: "Cvpr18 Visual Recognition and Beyond"
date: 2018-08-12T02:37:14Z
draft: true
---

https://sites.google.com/view/cvpr2018-recognition-tutorial
===========================================================

Learning deep representations for visual recognition
----------------------------------------------------
kaiming he

deep learning is representation learning.

represent (raw) data for machines to perform tasks:
vision(pixels), language(letters), speech(waves), games(status).

representation learning for alpha go: 3^361 states? bad representations.
for photos: 256^(3*640*480)? bad representations.

however, bad representations -> (models, now the neural network) -> good representations.

how was an image represented?

(shallow)
pixels -> classifier
pixels -> edges -> classifier
pixels -> (SIFT/HOG) (edges -> histogram) -> classifier
pixels -> edges -> histogram -> k-means, sparse code, FV/VLAD -> classifier
(deeper)

specialized components, domain knowledge required.

neural net: generic components, less domain knowledge.

lenet.

alexnet. lenet backbone plus relu, dropout, data augmentation.
relu: accelerate training, better grad prop v.s. tanh.
dropout: reduce overfitting. might be instead done by BN.

vgg-16/19.
modularized design: 3x3 conv.
stage-wise training: we need a better initialization.

initialization methods:
analytical formulations of normalizaing forward/backward signals.
based on strong assumptions (like gaussian distributions)
e.g. xavier init (linear), n * Var[w] = 1
e.g. msra init (relu), n * Var[w] = 2

googlenet/inception. accurate with small footprint
multiple branches. shortcuts. bottleneck (reduce dim by 1x1 before 3x3 and 5x5).

batch normalization (BN):
xavier/msra init are not directly applicable for multi-branch nets.
optimizing multi-branch convnets largely benefits from BN. (including all inceptions and resnets)
data driven normalization: greatly accelerate traininig, less sensitive to initialization, improve regularization.

resnets
overly deep plain nets have higher training error. a general phenomenon, observed in many datasets.
residual block.
practical design.

besnet beyond computer vision:
“Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation”.
“WaveNet: A Generative Model for Raw Audio”.
“Mastering the game of Go without human knowledge”,
resnext(inception+resnet): “Aggregated Residual Transformations for Deep Neural Networks”.
“Exploring the Limits of Weakly Supervised Pretraining”.

more architectures:
densenet, xception, mobile net, shufflenet.

teaser: “Group Normalization”. (motivation???)

20180704
