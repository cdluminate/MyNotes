Caffe tips
===

https://github.com/BVLC/caffe/wiki/Faster-Caffe-Training

https://github.com/BVLC/caffe/wiki/Fine-Tuning-or-Training-Certain-Layers-Exclusively

https://github.com/BVLC/caffe/wiki/Image-Format:-BGR-not-RGB

https://github.com/BVLC/caffe/wiki/Making-Prototxt-Nets-with-Python

https://github.com/BVLC/caffe/wiki/Model-Zoo

https://github.com/BVLC/caffe/wiki/Simple-Example:-Sin-Layer

https://github.com/BVLC/caffe/wiki/Solver-Prototxt

https://github.com/BVLC/caffe/wiki/Training-and-Resuming

https://github.com/BVLC/caffe/wiki/Using-a-Trained-Network:-Deploy

https://github.com/BVLC/caffe/wiki/Working-with-Blobs

* Be careful when training a network with a deploy version of network
prototxt. The default weight/bias initialization is zero-constant filling.
The training will fail without proper weight initialization. See `caffe.proto`
FillerParameter definition for detail.
