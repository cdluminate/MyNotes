Some CUDA tips
--------------

# CUDA doesn't work while `nvidia-smi` is working?

```
$ nvidia-smi # works
$ caffe device_query -gpu 0
I0127 03:24:20.986871 27178 caffe.cpp:138] Querying GPUs 0
F0127 03:24:21.092293 27178 common.cpp:152] Check failed: error == cudaSuccess (30 vs. 0)  unknown error
$ sudo caffe device_query -gpu 0 # works, CUDA 9.0.85, Nvidia 384.11
```

There is something wrong in driver: make sure every kernel modules are
loaded: nvidia-current-{uvm,drm,modeset}

reference: https://github.com/BVLC/caffe/issues/4543
