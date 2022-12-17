---
title: "Bits"
date: 2018-08-12T02:35:26Z
draft: true
---

Some of My Naive Bits and Questions
===================================

Tips about Adjusting Parameters
-------------------------------

-  Initial Learning Rate: determine it according to Andrej's thesis
   "connecting image and text".
-  Decaying Learning Rate: when you get a working model and a sensible
   set of parameters, a learning rate decaying with iterations
   increasing may help further improve the performance of your model.
-  Batch Normolization: may promote the model performance.

Naive points from a novice
==========================

-  ``stree2vec`` learning word representation in unsupervised manner
   with the help of syntax tree. New argument:
   treestructural-relationship(w-t, w). Ref:
   http://export.arxiv.org/pdf/1707.05005

-  not learning the weights but changing the rotation made by the weight
   matrix, while keeping the weight matrix orth.

-  Bits on Reading a Paper: Grasp the core idea first. The title of an
   article is the core idea in a word, but its too short and coarse to
   convey the author's concept. Generally this goal could be reached
   after reading the abstract and the main architecture description.

-  Promote a binary classifier to a 3-class classifier just like a
   growing child?

-  What characteristic does the embedding space learnt by
   softmax-supervised VGG-16 have? Does that characteristic compatible
   with our demand of aligning with treelstm embeddings in a common
   space?

-  Squared contrastive loss (repelling force). The gravity is squared.

- Standard classification loss functions, like the cross entropy loss with
  softmax activation, are not designed to learning good representation in
  terms of feature distance.

Questions, Whys and Whynots
===========================

1. why is :math:`(\hat{y} - y)` used in the MSE loss instead of
:math:`(y - \hat{y})`?

  Assume that :math:`\hat{y}` is larger than :math:`y`, then
  :math:`\hat{y} - y` is positve. The gradient of yhat w.r.t
  loss is hence positive. We want yhat to go along the opposite
  direction of the gradient, so yhat will become smaller after
  an update step. If yhat is smaller than y, then yhat will be
  bigger than y as expected. If we use the latter one, the
  gradient will get mess up.

图像文字联合嵌入的改进方法
==========================

预先生成M个n维矢量，使得任意两个不同向量的cos相似度小于1-margin。

1. 我们需要多少维？

在给定这些预分配矢量的情况下，分别使用最小二乘训练视觉嵌入模型和语言
嵌入模型。然后再finetune。
