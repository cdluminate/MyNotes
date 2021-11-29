
qemu/kvm
---

under `-nographic` mode
```
kvm -m 512 -hda hdd/archlinux-2016.05.01-dual.iso -nographic -serial mon:stdio
or
kvm -m 512 -kernel vmlinuz -initrd initrd -append "console=ttyS0' -nographic -serial mon:stdio
```
then add `console=ttyS0` kernel param in Grub.

seems archlinux iso can be used in this way.

```
qemu-system-x86_64 --enable-kvm -m 512 --cdrom archlinux-2016.05.01-dual.iso -nographic -serial mon:stdio -hda junk.img --boot order=c
```
