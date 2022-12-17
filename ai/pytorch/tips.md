Pytorch Tips
===

## Decaying learning rate

https://discuss.pytorch.org/t/adaptive-learning-rate/320

## TensorBoard?

`pip3 install visdom`

or

`pip3 install tensorboardX`

## CHW/HWC convertion without image rotation

```
Image -> Numpy : transpose((2,0,1))
HWC      CHW

Numpy -> Image : transpose((1,2,0))
CHW      HWC
```

## CUDA Memory is not freed.

That's because the dataloader doesn't stop its workers if you kill the process
abruptly. Make sure all the related processes get killed.
See https://github.com/pytorch/pytorch/issues/1085

## Dynamic and Static computation graph

https://pytorch.org/tutorials/beginner/pytorch_with_examples.html#tensorflow-static-graphs

## Custom module and loss function

http://pytorch.org/docs/master/notes/extending.html

http://pytorch.org/tutorials/beginner/examples_autograd/two_layer_net_custom_function.html

https://www.zhihu.com/question/66988664

https://stackoverflow.com/questions/44597523/custom-loss-function-in-pytorch

## What’s the behaviour of torch.util.data.DataLoader when num_worker=1?

is the data loaded in asynchronized manner?

Yes. The data is loaded asynchronizly. Serial data loaders will have inferior
performance compared to this one.

## Misc article

https://spandan-madan.github.io/A-Collection-of-important-tasks-in-pytorch/

http://blog.christianperone.com/2018/03/pytorch-internal-architecture-tour/
