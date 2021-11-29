Tips about Cross Compilation
===

# simple cross-compiling

an example for mips64el

```
CC=mips64el-linux-gnuabi64-gcc

with these packages
 1. gcc-mips64el-linux-gnuabi64
 2. libc6-dev-mips64el-cross
 3. qemu-user-binfmt 
```

# cross build with full chroot

an example for ppc64el

```
sudo apt install qemu-user-binfmt qemu-user-static
sudo debootstrap --arch=ppc64el unstable . https://mirrors.ustc.edu.cn/debian
schroot >
 [sid-ppc64el]
 type=directory
 directory=/mnt/sid-ppc64el
 profile=desktop
 users=lumin

schroot -c sid-ppc64el
```
