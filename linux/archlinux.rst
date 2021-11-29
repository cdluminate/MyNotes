ArchLinux Notes
===============

Installation with live CD
-------------------------

* download CD::

      https://www.archlinux.org/download/

* read guide::

      https://wiki.archlinux.org/index.php/Beginners%27_guide
      https://wiki.archlinux.org/index.php/Installation_guide

* boot with arch live CD

* make partitions

* mount target::

      mount /dev/sda3 /mnt
      mount /dev/sda2 /mnt/boot

* select a mirror::

      head -n1 /etc/padman.d/mirrorlist
      Server = http://mirror.example.org/archlinux/$repo/os/$arch

* install base system::

      pacstrap -i /mnt base base-devel [parted] [vim] ...

* generate fstab::

      genfstab -U /mnt > /mnt/etc/fstab

* chroot and configure::

      arch-chroot /mnt /bin/bash

      + uncomment en_US.UTF-8 UTF-8 in /etc/locale.gen
      + locale-gen
      + echo LANG=en_US.UTF-8 > /etc/locale.conf
      + link timezone
        ln -sf /usr/share/zoneinfo/UTC /etc/localtime
      + check time
        hwclock --systohc --utc
      + set hostname
        echo ArchLinux > /etc/hostname
      + set hosts
        echo 127.0.0.1 localhost > /etc/hosts
        echo ::1 localhost >> /etc/hosts
      + re-generate initramfs
        /etc/mkinitcpio.conf
      + change password
        passwd
      + install grub
        pacman -S grub os-prober
        grub-install --recheck /dev/sda
      + generate grub config file
        grub-mkconfig -o /boot/grub/grub.cfg

* finishing base system installation::

     + exit from chroot
     + umount -R /mnt
     + sync; reboot

* read post-installation wiki::

      https://wiki.archlinux.org/index.php/General_recommendations

* install X::

      https://wiki.archlinux.org/index.php/Xorg

      + pacman -S xorg xorg-server xorg-xinit
      + pacman -Ss xf86-video

* install [DM] slim::

      https://wiki.archlinux.org/index.php/SLiM

      + pacman -S slim
      [+] systemctl enable slim

* install i3-wm::

      https://wiki.archlinux.org/index.php/I3

      + pacman -s i3-wm dmenu i3status
      + write ~/.xinitrc
        exec i3

* try it out::

      + systemctl start slim
      + Ctrl^D xterm

      http://i3wm.org/docs/refcard.html
      http://i3wm.org/docs/userguide.html

Install from an existing Linux system
-------------------------------------

> https://wiki.archlinux.org/index.php/Install_from_existing_Linux  

* download bootstrap tarball
* extract to /tmp
* cd /tmp/root.x86_64/
* Setup /etc/pacman.d/mirrorlist
* sudo ./bin/arch-chroot .
* Init pacman keyring::

      + pacman-key --init
      + pacman-key --populate archlinux

* mount target filesystem::

      + mount /dev/sdb5 /mnt

* Complete base system::

      + pacman -Syy
      + pacstrap /mnt busybox base base-devel grub vim parted

Install Arch root on ZFS
------------------------

> https://wiki.archlinux.org/index.php/Installing_Arch_Linux_on_ZFS  
> https://wiki.archlinux.org/index.php/ZFS  

* boot with arch live cd
* configure mirrorlist
* enable AUR::

    pacman.conf

    [archlinuxfr]
    Server = http://repo.archliux.fr/x86_64
    SigLevel = Never

    [archzfs]
    Server = http://archzfs.com/$repo/x86_64
    SigLevel = Never

* install yaourt ``pacman -S yaourt``
* FIXME: archlinux broken?

ArchLinux with UEFI
-------------------

parted and filesystem::

    parted>
      mktable gpt
      mkpart 2mb 512mb name=UEFI type=fat32
      mkpart 512mb-100% name=ROOT type=ext4
      toggle 1 esp
    $ partprobe
    $ mkfs.ext4 /dev/sda2
    $ mkfs.vfat -F32 /dev/sda1
    $ mount /dev/sda2 /mnt
    $ mount /dev/sda1 /mnt/boot
    $ pacstrap /mnt base

    $ grub-install --efi-directory=/boot/efi --boot-directory=/boot /dev/sda
    # /boot/efi/EFI/arch/grubx64.efi
    $ efibootmgr

Troubleshooting
---------------

* pacman GPG error::

    error: GPGME error: No data
    error: failed to update community (invalid or corrupted database (PGP signature))

  set ``SigLevel = Never`` for ``[community]`` in this case. Note, this is a bad solution.

Arch Build System
-----------------

abs config file: `/etc/abs.conf`

example: rebuild dwm::

    sudo pacman -S base-devel
    sudo pacman -S abs

    sudo abs community/dwm
    cp -av /var/abs/community/dwm ~/packages
    cd ~/packages/dwm
    vim config.h
    vim PKGBUILD # change hashsum
    makepkg -f
    sudo pacman -U dwm-6.1-3.xxx.tar.gz


References
----------

* Archlinux.org
  Wiki.archlinux.org

* i3wm.org

* https://wiki.archlinux.org/index.php/VirtualBox#Launch_the_VirtualBox_guest_services
  This tells you how to make virtualbox arch work, incl. X11.

  example .xinitrc::

       /usr/bin/VBoxClient-all
       exec gnome-session

* Dependencies of wifi-menu::

      dialog wpa_supplicant

* Desktop Env : .xinitrc::

      /usr/bin/VBoxClient-all
      exec i3
      exec startkde
      exec gnome-session

* ABS::

   https://wiki.archlinux.org/index.php/Arch_Build_System
   https://wiki.archlinux.org/index.php/Pacman
   https://wiki.archlinux.org/index.php/PKGBUILD
