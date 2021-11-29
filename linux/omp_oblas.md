Note on OpenMP and OpenBLAS
===

# when running torch
please set openmp thread number according to your CPU or it will suck in performance.
```
OMP_NUM_THREADS=6 th test.lua
```

According to [openblas readme](https://github.com/xianyi/OpenBLAS#set-the-number-of-threads-with-environment-variables), we should use `OPENBLAS_NUM_THREADS` instead.

```
export OPENBLAS_NUM_THREADS=4
```

# openblas

re-compile openblas locally to gain better performance.

```
apt source openblas
vim rules
 -> export DEB_CFLAGS_MAINT_APPEND= -march=native # C
 -> export DEB_FFLAGS_MAINT_APPEND= -march=native # Fortran
debuild
```

To disable `DYNAMIC_ARCH` build, remove that flag. Enable dynamic
cpu detection with `DYNAMIC_ARCH=1` make flag.

# mkl

http://diracprogram.org/doc/release-12/installation/mkl.html
