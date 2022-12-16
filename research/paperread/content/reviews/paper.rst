---
title: "Paper"
date: 2018-08-12T02:44:27Z
draft: true
---

Computer Vision Papers
======================


Densely Connected Convolutional Networks
----------------------------------------
http://openaccess.thecvf.com/content_cvpr_2017/papers/Huang_Densely_Connected_Convolutional_CVPR_2017_paper.pdf

CVPR17 best paper

1. Whereas traditional convolutional networks with L layers
have L connections—one between each layer and its subsequent
layer—our network has L ( L +1) 2 direct connections.  For
each layer, the feature-maps of all preceding layers are
used as inputs, and its own feature-maps are used as inputs
into all subsequent layers.

2. Further, we also observe that dense
connections have a regularizing effect, which reduces over-
fitting on tasks with smaller training set sizes.

3. tochastic depth im-
proves the training of deep residual networks by dropping
layers randomly during training. This shows that not all
layers may be needed and highlights that there is a great
amount of redundancy in deep (residual) networks. Our pa-
per was partly inspired by that observation

20180531

Multimodal Convolutional Neural Networks for Matching Image and Sentence
------------------------------------------------------------------------
https://www.cv-foundation.org/openaccess/content_iccv_2015/papers/Ma_Multimodal_Convolutional_Neural_ICCV_2015_paper.pdf

1. special architecture is designed to solve the image-text matching problem as a binary classification problem.

n1. This paper tells us that aligning image and text representations with binary
classifier with pairwise sampling method is doable.

20180530

Learning Cross-modal Embeddings for cooking recipes and food images
-------------------------------------------------------------------
http://openaccess.thecvf.com/content_cvpr_2017/papers/Salvador_Learning_Cross-Modal_Embeddings_CVPR_2017_paper.pdf

1. this paper introduces a new dataset, named recipe 1M. The previous datasets are
limited in either generality or size.

2. food image - recipe embeddings. food image representations come from vgg and resnet.
word2vec representation for each ingredient. two-stage LSTM which is deisigned to encode a sequence
of sequences. skip-thought vector encodes a sentence and uses that encoding as context when docoding
or predicting the previous and next sentences.

3. food image - recipe joint neural embedding model. the loss function is a summation of
   cosine similarity loss and the proposed semantic regularization loss.
   https://pytorch.org/docs/stable/nn.html?highlight=cosine_sim#torch.nn.CosineEmbeddingLoss

4. semantic regularization. Essentially the model also learns to classify any image
or recipe embedding into one of the food-related semantic aategories.
The coefficient assigned to the semantic regularization loss is 0.02, but it
brings significant performance boost.

5. two-stage optimization procedure is used while learning the model. If two networks
are updated simutaneously, optimization becomes oscillatory and even divergent. 


n1: additionally, we demonstrate that regularization via the addition of a high-level
classification objective both improves retrieval performance to rival that of humans
and enables semantic vector arithmetic.

n2: section 3.1, use LSTM instead of GRU. why? Not explained.

20180530

Video Captioning with Transferred Semantic Attributes
-----------------------------------------------------
https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/Video-Captioning-with-Transferred-Semantic-Attributes.pdf

1. Most related works encodes the video with a CNN, and decodes the video
   representation with an RNN. Existing work includes template-based methods
   and generative (RNN) methods.
2. This works proposes to incorporate the transferred semantic attributes
   learnt from images and videos into the CNN/RNN framework.
3. The proposed model learns from three input sources: image, text, and attributes.
4. math:`E(v, A_i, A_v, S) = -log Pr(S|v, A_i, A_v)`, where v is repr(video),
   A_i is image attributes, A_v is video attributes, S is sentence.
   It is noted that since the sentence is a sequence, we can expand the
   log probability by using chain rule :math:`log Pr(S|v,A_i,A_v) = \sum_{t=1}^N log Pr(w_t|v,A_i,A_v, w_0, w_1, \ldots, w_t-1)`.
5. image attributes :math:`Pr_I^{w_a} = 1 - \prod_{r_i \in b_I} (1-p_i^{w_a})`
   Seems like a series of binary classifiers.

n1. mean pooling over the video frame representations looks questionable.

20180529

Surpassing human-level face verification performance on LFW with gaussian face
------------------------------------------------------------------------------

* lfw: 98.52%
* discriminative gaussian process latent variable model (GP)
* overfitting due to dataset bias
* face verification method (1) low-level feature + classification
  (2) DNN.
* TODO/FIXME

2018.05

Finding beans in burgers: Deep semantic-visual embedding with localization
--------------------------------------------------------------------------
https://arxiv.org/pdf/1804.01720.pdf

TAG: image-caption-retrieval state-of-the-art

1. Several works have proposed to learn a two-path neural network that maps
   images and texts, respectively, to a same shared Euclidean space where
   geometry captures useful semantic relationships. ... In the present work,
   we introduce a new architecture of this type, with a visual path that
   leverages recent space-aware pooling mechanisms.
2. the model can not only allow cross-modal retrieval, but also localize
   concepts.
3. "set of sentences unrelated to n-th image". UNRELATED??
4. hard negative is used in this work. following vsepp
5. beyond its parctical interest, thie hard negative mining strategy limits
   the amount of gradient averaging, making the training more discerning.
6. Smaller batches result in weaker perforamnce while too large ones prevent
   the model from converging.


note1. Combine localization and image captioning.

note2. Recall that in the VSE++ paper, fine-tuning the CNN side while keeping
       the RNN side frozen and using random crop gives a significant
       performance boost. That means the vision side really needs to be
       improved. In this paper, the authors proposed a method that combines
       idea of object localization, and got an even better performance.
       "we introduce a new architecture of this type, with a visual path that leverages recent space- aware pooling mechanisms."

note3. Simple Recurrent Unit is used (SRU) is this work.

note4. They borrowed the architecture of VSE++ and applied some modifications
on it. The so-called "object localization" stuff doesn't influence the embedding
learning at all! So, it is still a puzzle how that performance boost has came.
They are many possible causes: architecture change, batch size, learning rate,
dimensionality, etc.

note4. The highlight of this work is incorporating object-localization task
into image-text semantic embedding space learning algorithm.

2018.05

Improving pairwise ranking for multi-label image classification
---------------------------------------------------------------

1. [observation] ranking ~ hinge loss, non-smooth and difficult to optimize.
2. 2 techniques to improve pairwise ranking based multilabel classification.
   (1) a novel loss for pairwise ranking (easier to optimize)
   (2) label decision module
3. one popular approach: multi-label -> multiple binary label problems,
   however, label dependency, label sparsity, label noise
4. related: multilabel-classification, image annotation
5. pairwise ranking: flexibility (learning machines), empirical performance,
   (however) hinge loss function is non-smooth. (and) ranking objective does
   not fully optimize the multilabel objective.
   multi-label :math:`\min \sum_i I[\hat{Y}_i == Y_i]`
   or :math:`\min \sum_i |\hat{Y}_i \cup Y_i - \hat{Y}_i \cap Y_i|`
   or :math:`\min \sum\sum I[\text{rank}(y_{pos}) \prec \text{rank}(y_{neg})]`
   but the last method lacks label decisions. A common solution is to take
   topK as output where K is mannually set. This is problemaitc since the
   number of visual concepts depends on image content.
6. **Approach** dataset :math:`D=\{(X_i,Y_i)\}_{i=1}^N` where the i-th image
   :math:`X_i\in\Re^d`, and :math:`Y_i\subseteq \mathcal{Y}` where :math:`\mathcal{Y}`
   is the label set :math:`\mathcal{Y} \triangleq \{1,2,\ldots,k\}`.
   :math:`k=|Y_i|`. :math:`F(x)=g(f(x))`, where :math:`f(x):\Re^d\mapsto\Re^K`
   represents image to score function. :math:`g(f(x)):\Re^K\mapsto\Re^k`
   represents the label decision set.
7. **label prediction**: :math:`f(x;\theta)\in\Re^K`, optim
   :math:`\min_\theta \frac{1}{N} \sum_{i=1}^N l(f(X_i;\theta), Y_i) + R(\theta)`
   ranking loss :math:`f_u(X)>f_v(X), \forall u\in Y, v\notin Y`,
   :math:`\sum_{v\in Y_i}\sum_{u\notin Y_i} [\alpha + f_v(X_i) - f_u(X_i)]_+`
   is not smooth.

   The proposed ranking loss allows adaptive margin, and is differentiable,
   and smooth. The negative sampling :math:`\Phi(Y_i;t) \subseteq Y_i\otimes (\mathcal(Y)-Y_i)`
8. **Related loss functions**
   1. WARP, :math:`l_\text{warp}=\sum_{u\in Y_i}\sum_{v\notin Y_i} w(r_i^u)[\alpha+f_v(X_i)-f_u(X_i)]_+`
      but the author's observation is that there is no performance boost for
      the multi-label classification problem.
   2. BP_MLL, :math:`l_\text{BPMLL}=\sum_{u\in Y_i}\sum_{v\notin Y_i} \exp(f_v(X_i)-f_u(X_i))`
      cite Vapnik (statistical learning) hinge loss formulations usually generallize
      bettern than least square formulations.
9. **label decision**
   there are two versions of proposed decision module
   (1) (topk) estimates label count. cast as an n-way classification:
       :math:`l_{count} = -\log(softmax(\cdot))`
   (2) estimates the optimal threshold values for each class.
       cast as k-d regression.
       :math:`l_{thresh} = -\sum_{k=1}^K Y_{i,k} \log(S_\theta^K) + (1-Y_{i,k})\log(1-S_\theta^K)`

   the training process: CNN parameter fixed. jointly learning provides better
   performance.
10. *detail*: VGG16, 50 epoches, L2 5e-5, SGD mom 0.9 lr 1e-3

20180409

Deep captioning with multimodal recurrent neural networks (m-RNN)
-----------------------------------------------------------------
http://www.stat.ucla.edu/~junhua.mao/papers/m-RNN_iclr_camera_ready.pdf

1. This paper presents a multimodal recurrent neural network model that
   can be used for generating novel image captions and retrieving images
   or sentences.
2. Our work has two major difference from these methods.
   (1) incorporate a two-layer word embedding system in the m-RNN network
       structure which learns the word representation.
   (2) The image representation is inputted to the m-RNN model along with
       every word in the sentence description.
   (3) actually they use a modified RNN.
3. The network is trained with a classification loss. The retrieval task is
   done by ranking the conditional probability :math:`p(sentence|image)`.
4. This is an alchemy paper. Because there is no convincing explaination why
   the authors has made the changes to the model. Is a "state-of-the-art"
   experiment result enough for the novelty required by ICLR??? What the FUCK!

20180406


Neural Machine Translation by jointly learning to align and translate
---------------------------------------------------------------------
https://arxiv.org/pdf/1409.0473.pdf

1. Task: neural machine translation.
2. propose to extend the encoder-decoder architecture
   by allowing a model to automatically (soft-)search
   for parts of a source sentecne that are relevant to
   predicting a target word, without having to form
   these parts as a hard segment explicitly.
3. A potential issue with this encoder-decoder approach is
   that a neural network needs to be able to compress all
   the necessary information of a source sentence into a
   fixed length vector. This may make it difficult for the
   neural network to cope with long sentences, especially
   those that are longer than the sentences in the training
   corpus.
4. extension to the encoder-decoder model which learns to
   align and translte jointly. The most important
   distinuishing feature of this approach from the basic
   encoder-decoder is that it does not attempt to encode a
   whole input sentence intoi a single fixed-length vector.
   This model copes better with long sentences.
5. learning to align and translate
   1. Encoder is a bi-directional RNN. So that the hidden
      states contain the summaries of both the preceding
      words and the following words.
   2. attention decoder. TODO: notations
6. Experiment:
   1. dataset WMT14
   2. dim hid 1000.
   3. optim SGD + adadelta.
   4. generate using beam search.

20180406

Learning two-branch neural networks for image-text matching tasks
-----------------------------------------------------------------
https://arxiv.org/pdf/1704.03470.pdf

1. proposed two different network architectures.
   (1) two-branch embedding net with ranking loss
   (2) similarity network with regression loss
2. This TPAMI paper is an extension to its CVPR paper.
3. According to its experiments, similarity network performs
   worse than embedding netowrk by a margin.

20180405

Bi-directional block self-attention for fast and memory-efficient sequence modeling
-----------------------------------------------------------------------------------
https://arxiv.org/pdf/1804.00857.pdf

quick facts:
  1. new model for sequence encoding
  2. inexplicable?

20180405

Multi-lingual neural title generation for e-commerce browse pages
-----------------------------------------------------------------
https://arxiv.org/pdf/1804.01041.pdf
quick facts:
  1. industry application / implementation

20180405

Graph2Seq: Graph to Sequence Learning with attention-based neural networks
--------------------------------------------------------------------------
https://arxiv.org/pdf/1804.00823.pdf
quick facts:
  1. maps graph-structured inputs into a sequence output.

20180405

Efficient estimation of word representations in vector space (word2vec)
-----------------------------------------------------------------------
https://arxiv.org/pdf/1301.3781.pdf

1. two architectures for word similarity (syntactic and semantic)
2. distributed representations of words. neural network based language models
   significantly outperform N-gram models.
3. expectetation: not only similar words tend to be close to each other, but
   that words can have multiple degrees of similarity.
4. nouns can have multiple word embeddings, and if we search for similar words
   in a subspace of the original vector space, it is possible to find words
   that have similar endings. (cite)
5. vector arithmetic
6. NNLM architecture:
   1. focous on distributed representations of words learned by neural network
   2. all models: SGD and backpropagation
   3. input layer: n previous words -> one-hot vectors of size V
   4. projection layer: N*D
   5. hidden layer: N=10, H=500~2000
   6. output layer: size V
7. RNNLM
   1. no need to specify the context length
8. parallel training: async SGD and adagrad
9. NEW log linear models
   1. continuous repr, learned using simple model
   2. N-gram NNLM is trained on top of these distributed reprs
   3. Continuous Bag of Words, CBoW model: predicts current word based on the context
   4. Continuous skip-gram model: predicts surrounding words given current word.
10. It is possible to train high quality word vectors using very simple model
    architecture.
    
20180331

Semantic segmentation in 2017 (blog.qure.ai)
--------------------------------------------

Definition: Semantic segmentation is understanding an image at pixel level.
(classify each pixel). (done pixel-wise classification)

Datasets: VOC2012 and MSCOCO are most important SS datasets.

Approaches:
  1. before deeplearning; Texon Forest, Random Forest based classifier
  2. CNN enormous success.
     1. initial patch classification: cls pixel with a patch around it.
     2. (2014,FCN,Berkeley) paradigm; CNN without FC layer. faster than
        patch based methods. problem: pooling layers ("where" information loss).
        To handle this problem, two major ways have been developed.
        1. encoder-decoder architecture, e.g. U-Net
        2. dilated/atrous convolution (no pooling)
     3. CRF. can be used to improve segmentation (graphical model), i.e.
        i.e. to "smooth" the segmentation result.
        "similar intensity pixels tend to be labeled as the same class"
        e.g. Fully-connected CRF.

papers:
  1. FCN(2014): fully convolutional networks for semantic segmentation.
     * end to end CNN for SS
     * up sampling using deconvolutional layers
     * skip connection -> coarseness of upsampling
  2. SegNet(2015): a deep convolutional encoder-decoder architecture for image
     segmentation.
     * pooling indices transferred to decoder to improve performance.
     * more memory efficient than FCN.
  3. multi-scale context aggregation by dilated convolution
     * use dilated convolution (a kind of conv layer)
     * "context module" with uses dilated convolution for multi scale aggregation.
  4. deeplab v1 and v2 (2014, 2016)
     * dilated/atrous convolution; atrous spatial pyramid pooling (ASPP)
     * use fully connected CRF.
     * SIDENOTE: dilated conv. field of inception +, while num of parameter same.
  5. refineNet(2016)
     * dilated conv takes a lot of memory.
     * encode-decode architecture with residual connection
  6. PSPNet (2016)
     * pyramid pooling module to aggregate the context.
     * use auxilliary loss.
  7. (GCN) large kernel matters - improve semantic segmentation by global convolutional net (2017)
     * an encoder-decoder architecture with very large kernel convolutions
  8. deeplab v3 (2017)
     * atrous convolution VOC 2012 (score 85.7)

20180326

Sequence to sequence learning with neural networks (NIPS)
---------------------------------------------------------
https://papers.nips.cc/paper/5346-sequence-to-sequence-learning-with-neural-networks.pdf

* machine translation
* DNN inputs and targets, fixed dim. significant limitation.
* domain-independent.
* LSTM did not suffer on very long sentences.
* [important trick] reverse source sentences, (great boost), (time lag)
* The model
  1. RNN difficult to train due to long term dependencies
  2. goal of lstm
     ``p(y_1, ..., y_t'|x_1, ..., x_t) = \prod_{t=1}^T' p(y_t|v,y_1,...,y_t-1)``
     p represented by softmax output.
  3. special token ``<EOS>``
  4. 2 lstms, one for encoding, one for decoding
  5. multilayer LSTM used, outperforms shallow ones.
  6. it can have exploding gradients
* the experiment
  1. layer=4, 1000 cells, 1000d w2v, LSTM param ~U(-0.08, 0.08)
  2. SGD(0.7), 5 epoch, lr*0.5 every half epoch. 7.5 epoch.
  3. batch 128, gradient scaling due to exploding gradient.
  4. takes 10 days.
  
20180323

Show and tell: a neural image caption generator
-----------------------------------------------
https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Vinyals_Show_and_Tell_2015_CVPR_paper.pdf

* abbr NIC (neural image caption)
* CV and NLP (especially machine translation) 
* maximize likelihood ``P(sentence|image)`` while in MT ``P(T|S)`` is maximized. Simpler RNN leads to better result.
* contrib
  1. end to end, SGD-trainable.
  2. combine state of the art vision and language sub networks.
  3. significantly better than state of the art
* Model
  1. ``theta* = argmax_theta \sum_(I,S) log p(S|I;theta)``, where
    ``log P(S|I) = \sum_{t=0}^N log P (S_t|I, S_0, ..., S_t-1)``
  2. feeding the image at each time step as an extra input yields inferior result.
     overfits easily.
  3. ``loss(I,S) = - \sum_{t=1}^N log P_t(S_t)``
  4. inference: sampling and beam-search
* experiment
  1. embedding space is 512. both generation and ranking experiments were
     conducted.
 
20180323     


Unifying visual-semantic embedding with multimodal neural language models
-------------------------------------------------------------------------

https://arxiv.org/pdf/1411.2539v1.pdf https://github.com/ryankiros/visual-semantic-embedding

* Encoder-decoder structure
  (a) image-text joint embedding space
  (b) novel language model for decoding representation from the embedding space
  
* image caption generation and ranking, both.

* image caption generation methods: 3 types:
  (a) template-based (2) composition-based (3) neural net method
  
* image representation using the top layer before softmax. VGG19 on Imagenet.
  vector length 4096. word representation is pretrained BoW 300d.
  
* Pairwise ranking loss is used.

* log-bilinear neural language model (LBL) is quite straight forward.

* multiplicative neural language model (FIXME: Confusion)

* (contribution) SC-NLM, structure-context neural language model.
  soft template to help avoid the model from generating grammatical nonsense.
  
* [impl] arguments

  ::
  
    coco, margin=0.2, dim=1024, dim=image=4096, dim-word=300,
    max-epoch=15, grad_clip=2.0, batch=128, lr=2e-4, optim=adam
    
20180323


Learning Deep Structure Preserving Image-Text Embedding
-------------------------------------------------------
https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Wang_Learning_Deep_Structure-Preserving_CVPR_2016_paper.pdf

CVPR16 / image caption / cv18-cite

1. joint embedding image and text with a two branch network.
2. Traning cross-view ranking and within-view neighborhood structure
   preservation. (metric learning literature)
3. Metric: Dot product, i.e. Euclidean distance (L-2 normalized)
4. bi-directional ranking constraint: (1) d(x+, y+) + m < d(x+, y-)
   (2) d(x+, y+) + m < d(x-, y+)
5. structure preserving: (1) d(x+1, x+2) + m < d(x+1, x-)
   (2) d(y+1, y+2) + m < d(y+1, y-). How to find the neighbors?
   (different from tag-link)
6. section 2.2 (COCO) neighbor of image xi only contains xi itself.
   This is **problematic**.
7. Triplet sampling.
8. Paper about alchemy.

20170308

Some additional details.

  MSCOCO dataset. Margin set to 0.1 . 30 epoches to converge. sample triplets
  from minibatch.
  
  image -> subtract mean -> ten crop (224) -> vgg19 -> 10x4096 feature
  -> mean -> 4096 cnn feature vector as image representation
  
  sentence (fisher vector), 300-d word2vec -> ICA / HGLMM -> PCA
  
  evaluation: 1000 image / 5000 sentence. recall value (retrieval)
  
  Euclicean loss: max(0, m + xi yi - xi yk)
  Cosine similarity: max(0, m - xi yi + xi yk)
  
20180319, Mon

Semi-supervised Relational Topic Model for Weakly Annotat ed Image Recognition in Social Media
----------------------------------------------------------------------------------------------
https://www.cv-foundation.org/openaccess/content_cvpr_2014/papers/Niu_Semi-supervised_Relational_Topic_2014_CVPR_paper.pdf

CVPR2014 / image recognition, semi-supervised

1. Related work: explicit correspondence, image annotation. But, realistic
   scenarios images are weakly annotated (loosely related to the image).
2. Related work: pre-fusion at the feature level, post-fusion at the
   decision level. But, intrinsic relatoinshiops neglected.
3. link shared words, binary variable, positive realtion, negative relation.
4. only encode the relation for a subset of images. (1) tags noisy or missing.
   (2) fully connected network & computation cost.
5. selection of image relation, (1) large number of shared tag, more reliable.
   (2) top M/2 selected as positive relation. bottom M/2 (zero-shared) selected
   as negative relation.

20180305

Global and Local Consistent Age Generative Adversarial Networks
---------------------------------------------------------------
https://arxiv.org/pdf/1801.08390.pdf

Brief: Facial age generation by using GAN, together with several proposed application-specific adjustment and tricks.

Note: "Both global and local facial features are essential for the face representation."

20180127

Using Deep Autoencoders for Facial Expression Recognition
---------------------------------------------------------
https://arxiv.org/pdf/1801.08329.pdf

Brief: A good demo for autoencoder application. Lack of novelty.

20180127

Abnormal Heartbeat Detection Using Recurrent Neural Networks
------------------------------------------------------------
https://arxiv.org/pdf/1801.08322.pdf

Brief: Abnormal Heartbeat detection using existing Recurrent Neural Network. lack of novelty?
 
20180127

Understanding Human Behaviors in Crowds by Imitating the Decision-Making Process
--------------------------------------------------------------------------------
https://arxiv.org/pdf/1801.08391.pdf

Brief: Trajectory prediction by using GAN.

20180127

SELF-LEARNING TO DETECT AND SEGMENT CYSTS IN LUNG CT IMAGES WITHOUT MANUAL ANNOTATION
-------------------------------------------------------------------------------------
https://arxiv.org/pdf/1801.08486.pdf

The paper is poor in novelty. A detection and segmentation method for cysts
in lung CT image is proposed. Initially K-means is used to initialize a
detection / segmentation result, with K being the only hyper-parameter.
Next, a CNN called "U-Net" from a cited paper is trained with the K-means
result by optimizing an energy function.

- Lack of novelty, no enough work, no enough training detail, zero equation.
? Remind what on earth is "Detection" and "Segmentation".

20180126

SSD: Single Shot MultiBox Detector
----------------------------------
https://arxiv.org/pdf/1512.02325v2.pdf
http://www.cs.unc.edu/~wliu/papers/ssd_eccv2016_slide.pdf

eccv16 / detection

Synopsis: This paper proposed an approach for object detection with a single deep network
called SSD. It discretizes the output space of bounding boxes into a set of default
bounding boxes over different ratios and scales per feature map location. It will adjust
the box shape to better match the object shape on prediction. No bounding box proposal
is required. SSD is faster than the traditional 3-stage methods, and is easier to train.

Note, this paper cited YOLO (cvpr16)

20170905

Bringing Background into the Foreground: Making All Classes Equal in Weakly-supervised Video Semantic Segmentation
------------------------------------------------------------------------------------------------------------------
https://arxiv.org/pdf/1708.04400.pdf

iccv17 / video semantic segmentation

Synopsis: Focuses on the background class compared to previous works.

20170816

Cut, Paste and Learn: Surprisingly Easy Synthesis for Instance Detection
------------------------------------------------------------------------
https://arxiv.org/pdf/1708.01642.pdf

iccv17 / dataset generation, instance detection

Synopsis: A surprisingly easy dataset generation method is proposed. The performance
of the model trained by the generated dataset is promising.

20170816

Situation Recognition with Graph Neural Networks
------------------------------------------------
https://arxiv.org/pdf/1708.04320.pdf

iccv17 / graph neural network, situation recogonition

Synopsis: The paper proposed a Graph-based neural network model to capture the
joint dependency between the most salient verb and its corresponding roles.

20170816

Learning Feature Pyramids for Human Pose Estimation
---------------------------------------------------
https://arxiv.org/pdf/1708.01101.pdf

iccv17 / feature pyramids, pose estimation

Synopsis: This paper proposed a Pyramid Residual Module (PRMs) to enhance
the invariance in scale of DCNNs. The corresponding initialization scheme
is also carefully investigated.

20170815

MemNet: A Persistent Memory Network for Image Restoration
---------------------------------------------------------
https://arxiv.org/pdf/1708.02209.pdf

iccv17 / image restoration

20170814

Classifying Graphs as Images with Convolutional Neural Networks
---------------------------------------------------------------
https://arxiv.org/pdf/1708.02218.pdf>

? / Graph classification, graph kernel

20170814


Query-guided Regression Network with Context Policy for Phrase Grounding
------------------------------------------------------------------------
https://arxiv.org/pdf/1708.01676.pdf

iccv2017 / phrase grounding

20170812

Localizing Moments in Video with Natural Language
-------------------------------------------------
https://arxiv.org/pdf/1708.01641.pdf

iccv17 / video part retrieval

Synopsis: This paper aims at retrieving a specific temporal segment, or
 moment, from a video given a natural language text description.

20170812


Photographic Image Synthesis with Cascaded Refinement Networks
--------------------------------------------------------------
https://arxiv.org/pdf/1707.09405v1.pdf

iccv17 / image synthesis

Synopsis: This paper proposed a method to synthesis photographic images
conditioned on semantic layouts. It does not rely on adversarial, but
only a simple deep neural network architecutre. This method produces
much more realistic images compared to the other related works.

20170811

Weakly- and Self-Supervised Learning for Content-Aware Deep Image Retargeting
-----------------------------------------------------------------------------
https://arxiv.org/pdf/1708.02731.pdf

iccv17/ image retargeting

Synopsis: This is an enhanced version of image resizing...  WTH is this useful?

20170811

Learning to Disambiguate by Asking Discriminative Questions
-----------------------------------------------------------

iccv17 / VQA, disambiguate

Synopsis: This paper proposed a novel problem of generating discriminative
 questions to help disambiguate visual instances. In addition, a dataset
 is collected for this purpose.

20170811

Structured Attentions for Visual Question Answering
---------------------------------------------------
https://arxiv.org/pdf/1708.02071.pdf

iccv17/ VQA, attention

20170811


Temporal Dynamic Graph LSTM for Action-driven Video Object Detection
--------------------------------------------------------------------
https://arxiv.org/pdf/1708.00666v1.pdf

iccv17 / object detectoin, weakly supervised

Synopsis: Most existing works focus on using static image to learn object detectors,
while the pipeline proposed by this paper levarages action descriptions as the
supervision. For this purpose, a novel Graph LSTM framework is proposed to alleviate
the missing label issue.

20170811

Deep Metric Learning with Angular Loss
--------------------------------------
https://arxiv.org/pdf/1708.01682.pdf

iccv17 / triplet loss enhancement

Synopsis: This paper proposed an angular loss function, an enhanced version
of triplet loss function.

20170811, TODO

Two-Phase Learning for Weakly Supervised Object Localization
------------------------------------------------------------
https://arxiv.org/pdf/1708.02108.pdf

iccv17 / object localization, weakly supervised

Synopsis: This paper proposed two-phase learning to alleviate the problem that
only the most important parts of an object is localized. The first step finds
the most discriminative part of an image, and the second step finds the next
most important parts.

20170811

Training Deep Networks to be Spatially Sensitive
------------------------------------------------
https://arxiv.org/pdf/1708.02212.pdf

iccv17 / segmentation

Synopsis: This paper proposed a new metric for saliency prediction and segmentation
based on another one. Spatial information is incorporated into the objective, and
it is more efficient than the original one.

20170811

CoupleNet: Coupling Global Structure with Local Parts for Object Detection
--------------------------------------------------------------------------
https://arxiv.org/pdf/1708.02863.pdf

iccv17 / object detection

Synopsis: This paper proposed a RPN+CNN+RoI variant CoupleNet which couples the global
structure with local parts for boosting object detection.

20170810

Extreme clicking for efficient object annotation
------------------------------------------------
https://arxiv.org/pdf/1708.02750.pdf

iccv17 / annotation

Synopsis: Traditionally, to build a computer vision dataset (e.g. ILSVRC), the annotators
are asked to make bounding boxes. That is time-cosuming and a tight bounding box is
always not easy to make. This paper proposed "extreme clicking": the annotators are asked
to click four corners (top,bottom,left,right-most) of an object instead of annotating
bounding boxes. The resulting annotation is as good as the traditional ground truths,
an is less time-consuming for annotators.

20170810

SUBIC: A supervised, structured binary code for image search
------------------------------------------------------------
https://arxiv.org/pdf/1708.02932.pdf

iccv17 / Binary encoding, supervised

Synopsis: This paper proposed a method which leverages CNN to produce supervised
and structued binary encoding. Unlike those binary hashing schemes, this method
is supervised. WTH the author compare his supervised model with other unsup
methods?

20170810

PPR-FCN: Weakly Supervised Visual Relation Detection via Parallel Pairwise R-FCN
--------------------------------------------------------------------------------
https://arxiv.org/pdf/1708.01956.pdf

iccv/cvpr17 / visual relation detection, weak supervision

Synopsis: This paper proposed a PPR-FCN architecture for Weakly Supevised Visual
Relationship Detection (WSVRD).

20170810

Deep Binaries: Encoding Semantic-Rich Cues for Efficient Textual-Visual Cross Retrieval
---------------------------------------------------------------------------------------
https://arxiv.org/pdf/1708.02531.pdf

iccv17 / text-visual retrieval with binary encodings

Synopsis: This paper proposed a deep architecture for text-visual cross-modal retrieval.
Compared to other text-visual binary encoding methods, this paper put the focus on
the descriptive sentences. A combinatio of RPN+CNN+LSTM is used for the image encoding,
and a CNN is used for the text encoding.

Q: what will happen to the encoding if we shuffle the order of regions produced by RPN?

20170810

Binarized Convolutional Landmark Localizers for Human Pose Estimation and Face Alignment with Limited Resources
---------------------------------------------------------------------------------------------------------------
https://arxiv.org/pdf/1703.00862.pdf

iccv17 / binarized cnn block.

Synopsis: This paper proposed a binarized CNN block architecture that retains the
groundbreaking performance and suitable for limited computational resources.
A large number of ablation studies has been conducted.

20170809

GPLAC: Generalizing Vision-Based Robotic Skills using Weakly Labeled Images
---------------------------------------------------------------------------
https://arxiv.org/pdf/1708.02313.pdf

iccv17 / robotic skill, generalization, weakly labeled images

20170809

Unsupervised Video Understanding by Reconciliation of Posture Similarities
--------------------------------------------------------------------------
https://arxiv.org/pdf/1708.01191.pdf

cvpr/iccv17 / Posture, Action, Activity Similarity

Partial view: (1) learning a posture embedding. (2) sequence matching for
 self-supervision. (3) from local correspondences to a globally consistent
 posture representation. (4) RNN for learning temporal transitions.

20170808

Material Editing Using a Physically Based Rendering Network
-----------------------------------------------------------
https://arxiv.org/pdf/1708.00106.pdf

cvpr/iccv17 / image generation

Overview: This paper proposed an end-to-end image material editing model.
Given a single image of an object, several networks are used to predict
the material, the surface normals and the illuminations. Additionally
a desired target material is passed to the rendering layer along with
the items predicted from the given image to synthesize a target image.

20170806

Dual-Glance Model for Deciphering Social Relationships
------------------------------------------------------
https://arxiv.org/pdf/1708.00634.pdf

iccv/cvpr17 / ? / social relationship recognition.

Summary: Based on Fast-RCNN, RPN and RPN, this paper proposed a dual-glance
model for recognizing social relationship of persons of interest from still
images. The first glance uses a simple (R)CNN architecture and a softmax
classifier to produce a coarse prediction. The second glance uses CNN and
RPN to produce a set of features of region proposals. A weighting mechanism
is applied to the resulting regional feature set, and a fully-connected
network is used to give the final fine-grained prediction according to
these features. The predictions are aggregated by a simple function to
produce the final prediction of the second glance. The final prediction
of the two glances is a weighted sum of the individual glances.
The experiments are performed on their own dataset.
Apart from the Dual-Glance model, the paper contributed a novel People
in Social Context dataset.

20170805. Alchemy Paper.

Switching Convolutional Neural Network for Crowd Counting
---------------------------------------------------------
https://arxiv.org/pdf/1708.00199.pdf

ICCV|CVPR17 / ? / Crowd Counting

Summary: This paper proposed a model named Switch-CNN, where a switch classifier
is used to select a CNN regressor for the given image patch. The image patch is
then relayed to the selected CNN regressor to predict the corresponding crowd
density map. The proposed model were evaluated on several major datasets and
performed better than the state-of-the-art works.

20170804

Full-Network Embedding in a Multimodal Embedding Pipeline
---------------------------------------------------------
https://arxiv.org/pdf/1707.09872.pdf

? / Arxiv / Same as kiros

Summary: Based on Kiros' previous work, the authors replaced the convolutional
neural network embedding part with a full-network embedding part, which introduced
slight performance boost on recall of image annotation. However the recall
of image retrieval is low. Why is it?

20170804

Asymmetric Feature Maps with Application to Sketch Based Retrieval
------------------------------------------------------------------
https://arxiv.org/pdf/1704.03946.pdf

CVPR17 / Feature maps, sketch based retrieval

Summary: Not confident.

20170508

Improving Pairwise Ranking for Multi-label Image Classification
---------------------------------------------------------------
https://arxiv.org/pdf/1704.03135.pdf

CVPR17 / Image classification, pairwise ranking loss

Summary: (1) A variant of pairwise ranking loss is proposed in this paper,
which is smooth everywhere, unlike the original one (which uses hinge loss).
(2) A label decision module with learnable confidence threshould is
incorporated into the classifier to determine how many labels to output
instead of determined by a hand-crafted top-k rule. (3) Theoretical analysis
is provided.

20170505

Jointly Modeling Embedding and Translation to Bridge Video and Language
-----------------------------------------------------------------------
https://arxiv.org/pdf/1505.01861.pdf

CVPR15 / video -> description

::
     Arch:

     Video -> CNN -> mean pooling -> (1)
     Video -> 3D CNN -> mean pooling -> (2)
     (1)+(2) -> video representation (v)
     sentences -> sentences embedding (s)
     Wv -> E_relevance <- Ws
     v -> LSTM -> sentence -> E_coherence <- s

20170505

hierarchical multiscale recurrent neural networks
-------------------------------------------------
https://openreview.net/pdf?id=S1di0sfgl

ICLR17 / HM-RNN

Summary: pass

20170426

TREE-STRUCTURED DECODING WITH DOUBLY-RECURRENT NEURAL NETWORKS
------------------------------------------------------------------------------------------------------------
https://openreview.net/pdf?id=HkYhZDqxg

ICLR17 / tree generation

Summary: this paper proposed an architecture for restoring tree-structured
objects from encoded vector representations.

20170426 | same as I thought, but not confident about detail.


Detecting Visual Relationships with Deep Relational Networks <>`__
-------------------------------------------------------------------------------------------------------
https://arxiv.org/pdf/1704.03114.pdf

CVPR17 / visual relationship, DR-Net, CRF

Summary: Visual relationship detection, aims to locate all visual relationships
from a given image, and infer the (subject, predicate, object) triplets.
Most of previous methods treat this as a classification problem. One way
is to treat different combinations of objects and relationship predicates
as different clases. (too much classes, hard to train a classifier). An
alternative approach is to treat each type of relationship prediction as a
class. (too high inner-class diversity). This paper proposes a model to
address this problem, named Deep Relational Network (DR-Net), which outperforms
the state-of-the-art by a large margin.

::

    Arch: 3 Stages
     (1) object detection: Image -> many bounding box & appearance feature pairs
     (2) pair filtering: n pairs -> NN -> filtered pairs (number < n(n-1) )
     (3) foreach pair, fed to joint recognition module:
         [dual spatial masks -> spatial module -> spatial feature vector]
         [bbox -> apperance module -> appearance feaure vector]
         [concat(spatial feat, appr feat) -> NN -> compressed pair feature]
         [[subject feat, object feat, compressed pair feat] -> DR-Net]
     (4) DR-Net -> triplets

Note, model detail not confident

20170424

AttendtoYou: Personalized Image Captioning with Context Sequence Memory Networks
--------------------------------------------------------------------------------
https://arxiv.org/pdf/1704.06485.pdf

CVPR17 / Image captioning, personalization / Code available

Summary: This paper aims at addressing the personalization issue of image
captioning. This approach gives a descriptive sentence to describe a given
image, where some prior knowledge are taken into account, including
(1) user's active vocabulary (2) user's writing style. To accomplish that,
this paper proposes a novel model named Context Sequence Memory Network (CSMN),
which could be used in (1) hashtag prediction (2) post generation.

not confident at model detail.

20170424

Generating Multi-Sentence Lingual Descriptions of Indoor Scenes
---------------------------------------------------------------
https://arxiv.org/pdf/1503.00064.pdf

BMVC / Image paragraph, scene graph

Motivation: Single sentence is not sufficient for describing complex scenes.

Summary: This paper proposes a framework for generating multiple coherent
sentences according to a given image.

Architecture: (1) RGB-D image -> (visual models) -> scene graph -> semantic
trees -> generated description. (2) Reference Description -> parse graphs ->
semantic trees -> (generative grammar) -> generated description.
Where the visual model is a holistic 3D visual parser that converts RGB-D
image to semantics represented by scene graph (3D object detection -> holistic
CRF model -> scene graph). When generating lingual descriptions, the scene
graph is converted to a sequence of semantic trees, then descriptions are
generated by template from root to terminals along the topology of trees.

20170418, need details

This paper sucks in details. The method of converting a scene graph to
semantic tree is quite unclear.

20170423


Learning and Transferring Mid-Level Image Representations using Convolutional Neural Networks
---------------------------------------------------------------------------------------------

CVPR14 / CNN, transfer learning

Summary: This paper shows how image representations learned with CNNs on
large-scale annotated datasets can be efficiently transfered to other visual
recognision tasks with limited amount of data.

20170417

Age Estimation by Multi-scale Convolutional Network
---------------------------------------------------

CAS / ACCV14 / CNN, Age estimation

Summary: This paper proposes a CNN-based method for the age estimation problem.
The multi-scale strategy is introduced from traditional methods (incl. BIF) to CNN.

Architecture: Image -> facial landmarks -> local aligned multi-scale patches
-> Multi-scale CNN (Multi Input Multi Output) -> Predicted Age, Gender and
Ethicity.

Misc Notes: (1) For facial landmark localization, ASM/AAM was defeated by
newer ESR and its variants. (2) This paper decalres that color information is
unstable. (3) CNN performs better than previous state-of-the-art BIF-based
method, as concluded by this paper.

20170417

Rich feature hierarchies for accurate object detection and semantic segmentation
--------------------------------------------------------------------------------

Ross / CVPR? / R-CNN, object detection

Summary: This paper proposes a simple and scalable detection algorithm, named R-CNN.

Architecture: Image -> Extract Region Proposals -> CNN -> Classify regions with linear SVM.

20170416

Deep Learning Face Attributes in the Wild
-----------------------------------------
https://arxiv.org/pdf/1411.7766v1.pdf

? / CNN, Face localization, Face Attribute

Summary: This paper proposes a novel deep learning framework for face
attribute prediction in the wild.

Architecture: Image -> LNet 0 -> LNet s -> ANet -> FC -> Linear Classifier (SVM).
Where CNN LNet is for face localization, and CNN ANet is for attribute
prediction. The two CNNs are cascaded.

Misc Notes: (1) When training a model in cascaded manner, pre-training
strategies can improve CNN performance. (2) LNet's responce maps over the
entire image have strong indication of face's location. (3) High-level
hidden neurons of ANet automatically discover semantic concepts after
pre-training.

20170416

Scene Graph Generation by Iterative Message Passing
---------------------------------------------------
http://vision.stanford.edu/pdf/xu2017cvpr.pdf

feifei / CVPR17 / Scene graph generation

Summary: Scene graph is a visually-grounded graph over the object instances in
an image, where the edges depict their pairwise relationships. Scene graph
generation goes beyond object detection in isolation, which has a drawback:
it struggles to perceive the subtle difference between "a man feeding a horse"
and "a man standing by a horse". To capture this intuition, a joint inference
framework to enable contextual information to propagate through the scene
grpah topology via a message passing scheme is proposed. Let C denote a set
of classes, and R denote a set of relationship types, and all variables
are denoted as X={classi in C, bboxi in Re-4, itoj_type in R | i for all
proposal boxes, j for all proposal boxes}. This function needs to be
optimized, optimal x-* = argmax x Pr(X | Image, Bbox of image) . This model
performed iterative message passing between the primal and the dual sub-graph
along the topological structure of a scene graph.

Architecture: Image -> CNN+RPN -> Object proposal -> Graph inference ->
Scene graph. The CNN+RPN part produces (1) object class label (2) 3 bbox
offsets.

Misc notes: (1) As shown in previous work, dense graph inference can be
approximated by mean field in Conditional Random Fields (CRF). (2) Gated
Recurrent Unit (GRU) is used in this paper.

20170415

SPICE: Semantic Propositional Image Caption Evaluation
------------------------------------------------------
http://users.cecs.anu.edu.au/~sgould/papers/eccv16-spice.pdf

ECCV16 / SPICE, scene graph, image caption metric

Summary: This paper proposes a new automatic caption evaluation metric defined
over scene graphs coined SPICE, which captures human judgements better than
other automatic metrics.

Architecture: Both reference and candidate sentences are mapped through
dependency parse trees to sementic scene graphs (a kind of semantic
representation). Caption quality is determined using an F-score calculated
over tuples in the cnadidate and reference scene graphs.

Misc points: (1) The proposed method overcomes the n-gram problem.
(2) semantic graphs can be parsed from natrual language description.
(3) a common framework for semantic graphs: abstract meaning representation.

20170414

A Hierarchical Approach for Generating Descriptive Image Paragraphs
-------------------------------------------------------------------
https://arxiv.org/pdf/1611.06607v1.pdf

Feifei / CVPR17 / Image paragraph

Summary: Traditional sentence-level image captioning, which produces a sentence
describing a given image, always generates coarse sentences which lacks detail.
Densecap, as proposed recently, produces a set of sentences related to the given
image, however the resulting sentences are scattered in topic, and cannot tell
a coherent story about the given image, i.e. they do not form a cohesive whole
describing the entire image. Image paragraph, proposed in this paper, aims at
generating a paragraph describing the given image.

Architecture: Given an image, a region detector detects regions of interest
and produces features for each. Region features are projected to R-P, pooled
to give a compct image representation, and passed to a hierarchical RNN
language model comprising a sentence RNN and a word RNN. The sentence RNN
determines the number of sentences to generate based on the halting distribution
p_i, and also generate sentence topic vectors, which are consumed by each word
RNN to generate sentences.

Misc points: (1)To what extent does describing images with paragraphs differ
from sentence-level captioning? This is illustrated by dataset analysis.
(2) A heirarchical RNN is proposed to avoid the long time-scale problem, which
makes learning an appropriate representation much more tractable. (3) Two
transfer learning methods are used in this paper to initialize parameters.

20170413

Discriminative Neural Sentence Modeling by Tree-Based Convolution
-----------------------------------------------------------------
https://arxiv.org/pdf/1504.01106.pdf

/ ? / Tree Based CNN, Discriminative Sentence Modeling

Summary: (1) This paper combines the advantage of CNN and RNN together.
(2) structural information can be learned effectively.
(3) cnn does not use structure information explicitly.

Strength: (1) Combine advantages of RNNs and CNNs (TBCNN), for discriminative
sentence modeling. CNN is good at short propagation paths. RNN is good at
encoding structure information. (2) Several heuristics for pooling are proposed
for pooling along a tree structure.

Weakness: (x) No theoretical explaination...

20170409

A C-LSTM Neural Network for Text Classification
-----------------------------------------------
https://arxiv.org/pdf/1511.08630.pdf

// CNN, LSTM, Text Classification

Abs: Combine the strengths of CNN and LSTM and propose a model for sentence
representation for text classification.

20170409

When Are Tree Structures Necessary for Deep Learning of Representations?
------------------------------------------------------------------------
https://arxiv.org/pdf/1503.00185.pdf

? / EMNLP 2015 / TreeLSTM; NOTE

This paper benchmarks recursive neural models against sequential recurrent neural
models, by investigating four NLP tasks. Noticeable points: (1) Tree models tend
to help more on long sequences than shorter ones with sufficient supervision.
(2) Adopting bi-directional versions of recurrent models seem to largely
bridge the gap, producing equivalent or sometimes better results.
(3) Recurrent models like LSTMs can discover implicit recursive compositional structure.

However, as said by the authors, their benchmarking method may be "unfair".
In that case the conclustions should be suspected.

20170408

Enhancing and Combining Sequential and Tree LSTM for Natural Language Inference
-------------------------------------------------------------------------------
https://arxiv.org/pdf/1609.06038.pdf

? / ? / LSTM, TreeLSTM, Natural Language Inference (NLI)

This paper proposed a model that incorporates sequential LSTM and Tree LSTM
for natural language inference. Tree LSTM works as an auxiliary part in
proposed hybrid inference model, where its predicted probability is
averaged with that from sequential LSTM.

20170408

Skip-Thought Vectors
--------------------
http://papers.nips.cc/paper/5950-skip-thought-vectors.pdf

NIPS ? / Unsupervised Sentence Encoder.

20170405

Learning Deep Structure-Preserving Image-Text Embeddings
--------------------------------------------------------
http://slazebni.cs.illinois.edu/publications/cvpr16_structure.pdf

CVPR2016 / LSTM, Image Captioning

This paper has proposed an image-text embedding method in which a two-branch network
with multiple layers is trained using a margin-based objective function
consisting of bi-directional ranking terms and structure-preserving terms
inspired by metric learning.

One of its contributions is the modified version of pairwise ranking loss.

20170403

LSTM: A Search Space Odyssey
----------------------------
https://arxiv.org/pdf/1503.04069.pdf

TNNLS 2016 / LSTM, Odyssey

Eight LSTM variants are tested and compared via 5400 experiments in total.
None of its variant can improve upon standard LSTM significantly. Forget gate
and output activation function are the most critical components.

However the learning rate selection range $`[1.0\times 10-{-2},1.0 \times 10-{-6}]`$
is not explained and hence its significance in importance is suspected.

LSTM formulas are provided by its appendix A, including forward pass and backward pass. (TODO)

20170401


HYBRID SPEECH RECOGNITION WITH DEEP BIDIRECTIONAL LSTM
------------------------------------------------------
http://www.cs.toronto.edu/~graves/asru_2013.pdf

Automatic Speech Recognition and Understanding (ASRU) / Speech recognition, LSTM

A brief introduction to Recurrent Neural Network (RNN), Bi-directional
RNN (BRNN), Deep RNN (DRNN), Long-Short Term Memory (LSTM), Bi-directional
LSTM (BLSTM) and Deep BLSTM (DBLSTM) could be found in this article.

During training some Gaussian noise is added to network weights, and doing so improves generalization of the network.

20170331

Framewise Phoneme Classification with Bidirectional LSTM and Other Neural Network Architectures
-----------------------------------------------------------------------------------------------
https://www.researchgate.net/profile/Alex_Graves/publication/7647316_Framewise_phoneme_classification_with_bidirectional_LSTM_and_other_neural_network_architectures/links/00b7d51704ddf9793d000000.pdf

Neural Networks 2005 / LSTM, BPTT, Phoneme Classification

Bi-directional networks are better than unidirectional ones.

This paper contains a useful section `APPENDIX A: PSEUDOCODE FOR FULL GRADIENT LSTM`. (TODO)

20170331
