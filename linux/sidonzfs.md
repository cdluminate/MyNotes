Debian Sid root on ZFS
===

```
Copyright (C) 2016 Zhou Mo <cdluminate@gmail.com>  
MIT License
```

> https://github.com/zfsonlinux/zfs/wiki/HOWTO%20install%20Debian%20GNU%20Linux%20to%20a%20Native%20ZFS%20Root%20Filesystem  
> https://wiki.archlinux.org/index.php/ZFS  
> https://wiki.archlinux.org/index.php/Installing_Arch_Linux_on_ZFS  

## Installation Scheme

```
/dev/sda GPT
 - /dev/sda1: 2mb-4mb, toggle bios_grub
 - /dev/sda2: 4mb-256mb, ext4, to be used as /boot
 - /dev/sda3: 256mb-100%, zfs as /
```

Note, no swap here.

## Environment

* Host: Debian Sid (Sept. 2016)  
* USB Stick x1 (>= 2G)  
* QEMU  
* Official Debian zfs packages (`spl-dkms_0.6.5.8-1`, `zfs-dkms_0.6.5.8-1`, ...)  

Note, I perform this experiment on USB stick instead of disk image
because `losetup` will not load partition table in disk image file by default.
It supports `losetup --partscan` but I didn't tested it. On the contrary,
USB device is handy enough for me.

# Installation

#### Prepare environment

On the host machine we first install some packages.
```
$ sudo apt update
$ sudo apt install zfsutils-linux   # official ZFS packages
$ sudo apt install qemu             # vm with usb disk as sda
$ sudo apt install debootstrap      # minimal debian system
$ sudo apt install parted           # ...
$ sudo apt install grub2            # ...
```

#### Disk Partitioning

My USB stick is recogonized as `/dev/sdc` on host machine.
```
$ sudo parted --list
$ sudo parted /dev/sdc
parted>
  mktable gpt
  mkpart 2mb-4mb, toggle bios_grub, label bios_grub, no FS
  mkpart 4mb-256mb, label /boot, ext4
  mkpart 256mb-100%, label ZFS, zfs
$ sudo partprobe
```

Method2:
```
$ dd if=/dev/zero of=debian.img bs=1M count=3000
$ sudo parted debian.img
parted>
  ...
$ sudo losetup -P -f debian.img
$ lsblk
  loop0       7:0    0     3G  1 loop 
  ├─loop0p1 259:0    0     2M  1 loop 
  ├─loop0p2 259:1    0   240M  1 loop 
  └─loop0p3 259:2    0   2.7G  1 loop 
```

#### Make Filesystem

```
$ sudo mkfs.ext4 /dev/sdc2             # /boot
$ sudo zpool create -o ashift=9 -o altroot=/mnt -m none rpool /dev/disk/by-id/usb-XXXXX:part3
$ sudo zfs create -o mountpoint=none   rpool/ROOT
$ sudo zfs create -o mountpoint=/      rpool/ROOT/debian
$ sudo zfs create -o mountpoint=/home  rpool/home
$ sudo zpool set bootfs=rpool/ROOT/debian rpool
$ sudo zpool export rpool
```

Method2:
```
mkfs.ext4 /dev/loop0p2
cryptsetup benchmark
cryptsetup luksFormat /dev/loop0p3
cryptsetup luksOpen /dev/loop0p3 luks
zpool create -o altroot=/mnt -m none rpool /dev/mapper/luks
zfs create -o mountpoint=none rpool/ROOT
zfs create -o mountpoint=/ rpool/ROOT/debian
zpool set bootfs=rpool/ROOT/debian rpool
zpool export rpool
```

Note, `ashift=9` for 512 byte sector size while `ashift=12` for 4k sector size.

#### Bootstrap base system

```
$ sudo zpool import -o altroot=/mnt rpool
$ sudo mkdir -p /mnt/etc/zfs/
$ sudo zpool set cachefile=/mnt/etc/zfs/zpool.cache rpool
$ sudo mkdir -p /mnt/boot
$ sudo mount -t ext4 /dev/sdc2 /mnt/boot
$ sudo eatmydata -- debootstrap sid /mnt/ http://ftp.xdlinux.info/debian
```

Method2:
```
zpool import -o altroot=/mnt rpool
mkdir
zpool set cachefile=/mnt/etc/zfs/zpool.cache rpool
mkdir
mount -t ext4 /dev/loop0p2 /mnt/boot
bootstrap

OH MY GOODNESS, why is ZFS over LUKS so slow on my side?
https://mthode.org/posts/2013/Sep/gentoo-hardened-zfs-rootfs-with-dm-cryptluks-062/
https://help.ubuntu.com/community/encryptedZfs
```

#### Base system configuration

```
$ echo Solaris | sudo tee /mnt/etc/hostname
$ sudo cp /etc/resolv.conf /mnt/etc/
$ sudo vim /mnt/etc/fstab
vim>
  rpool/ROOT/debian  /      zfs   defaults  0  0
  /dev/sda3          /boot  ext4  defaults  0  0

$ sudo mount --bind /proc /mnt/proc
$ sudo mount --bind /sys  /mnt/sys
$ sudo mount --bind /dev  /mnt/dev
$ sudo chroot /mnt bash

chroot# passwd root

chroot# apt install vim

chroot# sudo vim /etc/apt/sources.list
chroot.vim>
  deb http://ftp.xdlinux.info/debian sid main contrib non-free

chroot# apt install locales
chroot# dpkg-reconfigure locales

chroot# apt install linux-image-amd64 linux-headers-amd64
chroot# apt install build-essential

chroot# apt install spl-dkms spl

chroot# apt install zfs-dkms
chroot# apt install zfsutils-linux zfs-initramfs

chroot# update-initramfs -k all -u
chroot# exit
```

#### Install GRUB

```
$ sudo grub-install --boot-directory=/mnt/boot /dev/sdc
```

#### Unmount devices

```
$ sudo sync
$ sudo umount /mnt/*
$ sudo zpool export rpool
```

#### Emulate with QEMU

```
$ sudo qemu-system-x86_64 --enable-kvm -m 1024 -hda /dev/sdc
```

#### Boot the system

```
qemu>
 grub>
  ls
  linux (hd0,gpt2)/vmlinuz-4.7.0-1-amd64 boot=zfs root=rpool/ROOT/debian ro vga=773
  initrd (hd0,gpt2)/initrd.img-4.7.0-1-amd64
  boot
 sid>
  $ sudo vim /boot/grub/grub.cfg
  vim>
   timeout=5
   linux (hd0,gpt2)/vmlinuz.............................
   initrd (hd0,gpt2)/initrd.............................
  $ sudo dhclient ens3
  $ sudo apt install ...................................
  $ sync; systemctl reboot
```
