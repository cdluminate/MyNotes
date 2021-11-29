Alpine Linux Note
=================

1. Alpine v3.4.
2. Alpine is very light-weighted.
3. Alpine uses ``musl`` as its libc.
4. Alpine uses ``busybox`` as its basic utils.
5. Alpine package management tool is ``apk``.
6. Alpine updates and upgrades with command ``apk update; apk upgrade``.

`Alpine Linux <https://wiki.alpinelinux.org/wiki/Main_Page>`__

-  After boot with cdrom, run this to install system

::

    setup-alpine

-  Configure ``/etc/apk/repositories``, adding the package source there,
   where the source URL can be local file e.g. ``/media/cdrom/apk`` or
   HTTP links e.g. ``http://192.168.0.1:8000/``.

-  Installing and removing software

::

    # apk add SOFTWARE
    # apk add openssh fail2ban htop man vim parted ppp
    # apk add utils-linux iproute2 pciutils usbutils coreutils binutils findutils grep
    # setup-xorg-base # installs xorg
    # apk add xorg-server xf86-video-vesa xf86-input-evdev xf86-input-mouse xf86-input-keyboard udev
    # apk add pacman
    # apk del pacman

    ### setup awesome
    # apk add slim
    # apk add awesome
    # apk add feh lua lxterminal

-  install compiling chain

::

    # apk install build-base gcc abuild bintuils cmake

-  apache2

::

    apk add apache2
    addgroup apache
    rc-service apache2 start
    curl -s localhost
    rc-update add apache2 default # start service on boot

-  traffic monitoring

::

    apk add iptraf-ng iftop ntop

-  https://wiki.alpinelinux.org/wiki/Fault\_Tolerant\_Routing\_with\_Alpine\_Linux
