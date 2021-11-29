FreeBSD Tips
============

https://www.freebsd.org/doc/en_US.ISO8859-1/books/handbook/

FreeBSD 11.1
------------

Basics

  Users and groups: `adduser, rmuser, su, chpass, passwd, pw, id`

  Files and permissions: `ls, chmod, chflags`

  Filesystem: `mount, umount`

  Process: `ps, top, kill`

  Shell: `chsh`

  Editor: `ee, vi`

Software Installation

  package::

    pkg search PKG
    pkg info PKG
    pkg install PKG
    pkg delete PKG
    pkg upgrade PKG
    pkg autoremove

  port/portsnap::

    cd /usr/ports
    make search name=lsof
    make quicksearch name=lsof

    portsnap fetch
    portsnap extract
    portsnap fetch update

    cd /usr/ports/sysutils/lsof
    make install
    make clean
    make deinstall

X Window System

  installing xorg::

    pkg install xorg

  the x display manager::

    /etc/ttys
    ttyv8 "/usr/local/bin/xdm -nodaemon" xterm off secure

  install gnome or mate::

    pkg install gnome3/mate
    vim ~/.xinitrc
      exec /usr/local/bin/mate-session

  suckless tools are available::

    pkg install dwm dmenu sterm

System Administration

  rc::

    /etc/rc.conf
    XXX_enable="YES"

    dbus_enable="YES"
    service dbus status
    service dbus start

  network::

    ifconfig

  etc layout::

    resolv.conf
    hosts

Security

  openssh

  ACL

  sudo

Jails

Storage

  gpart

GEOM: Modular Disk Transformation Framework

ZFS: The Z File System

  this is a good read
  https://www.freebsd.org/doc/en_US.ISO8859-1/books/handbook/zfs-advanced.html

Virtualization

  FreeBSD as a Guest on Virtualbox::

    cd /usr/ports/emulators/virtualbox-ose-additions
    make install clean

    rc.conf:
    vboxguest_enable="YES"
    vboxservice_enable="YES"

Updating and Upgrading FreeBSD

DTrace

Network Server

  inetd ...

Firewalls

  PF / IPFW / IPF

Tips

  List disks and partitions: ``geom disk list``, ``geom part list``

  Kernel source: ``src.txz from mirror site``

  Change mirror: https://mirrors.ustc.edu.cn/help/freebsd-pkg.html

  https://www.vultr.com/docs/how-to-secure-freebsd-with-pf-firewall
