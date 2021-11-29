UEFI Installation
===

some packages related to efi/uefi
```
grub-efi
  grub-efi-ia32
  grub-efi-amd64
efibootmgr
```

# Reference

> GNU :: grub :: doc  
> https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface  
> https://wiki.archlinux.org/index.php/GRUB/EFI_examples  
> https://wiki.archlinux.org/index.php/VirtualBox#Installation_in_EFI_mode  
> https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface  

# Debian Sid with EFI

The Debian installer handles UEFI properly.
```
sda gpt
sda1 512mb FAT32 esp,boot  /boot/efi       # mkfs.fat -F32 /dev/sda1
sda2 512mb ext4  boot      /boot
sda3 rest  ext4  root      /

efibootmgr
```

# inplace convertion from UEFI installation to BIOS installation
Initially I installed Debian/Sid on an UEFI machine with an ASUS X99-E WS motherboard,
however for some reason I moved the SSD from that machine to another with an ASUS Z10PE-D8 WS motherboard,
and the new motherboard supports no UEFI. Hence the boot failure.
```
sda GPT
 - sda1 esp,boot /boot/efi
 - sda2 /boot
 - sda3 /

parted /dev/sda
 - rm 1
 - mkpart 2mb-4mb, toggle bios_grub on
 - grub-install again on sda

update-grub2
reboot
```

# ArchLinux with EFI / bootctl

TODO

# Virtualbox EFI

write a script `startup.nsh` to avoid manual boot.

# see also

[archlinux with UEFI](./arch.md)  
