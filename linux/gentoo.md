Gentoo's Install Manual is valuable
===

Even to experienced administrators.

# Important notes

`emerge-webrsync` is shockingly faster than `emerge --sync`. It's a trap.

# Gentoo install node
> https://wiki.gentoo.org/wiki/Handbook:AMD64  

* choosing installation media, e.g. `install-amd64-minimal-20161006.iso`.  

Burn CD, note there are many kernel parameters available on boot failure from CD: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Media  

* boot from CD.  
* configure the network.  
* prepare the disks.  
* create file systems.  
* download stage3 tarball, e.g. `stage3-amd64-nomultilib-20161006.tar.bz2`.  

Use `links` to browse and download in textmode.

* unpack stage tarball. `tar jxvpf ......tar.bz2 --xattrs`  
* configure compile options. `vim /mnt/gentoo/etc/portage/make.conf`.  

CFLAGS, CXXFLAGS, MAKEOPTS

* install gentoo base system.  

set up GENTOO_MIRRORS and portage. Copy resolv.conf.

```
/etc/portage/make.conf
GENTOO_MIRRORS="https://mirrors.tuna.tsinghua.edu.cn/gentoo"
emerge-webrsync
emerge vim
```

* mount
```
root #mount -t proc proc /mnt/gentoo/proc
root #mount --rbind /sys /mnt/gentoo/sys
root #mount --make-rslave /mnt/gentoo/sys
root #mount --rbind /dev /mnt/gentoo/dev
root #mount --make-rslave /mnt/gentoo/dev
```

TODO

# Gentoo Prefix
