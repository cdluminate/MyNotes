cpio
---

decompress into cwd
```
cpio -idmv < initrd.cpio
```

or just
```
unar some_cpio.img
```

for initramfs
```
lsinitramfs /boot/initrd.img
```
