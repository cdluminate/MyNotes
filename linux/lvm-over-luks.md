LVM over LUKS
---

Debian Installer, expert install method supports it.  
"guided partition with LVM and encryption".
It is also easy to manually set LVM over luks with that installer.

There is no notable difference for `fstab`:
```
/dev/mapper/debian-vg-root / ext4 errors=remount-ro 0 1
UUID=<UUID> /boot ext2 defaults 0 2
/dev/mapper/debian-vg-home /home ext4 defaults 0 2
/dev/mapper/debian-vg-swap none swap sw 0 0
/dev/sr0 /media/cdrom0 udf,iso9660 user,noauto 0 0
```
and there is no notable difference in grub config, either.
```
linux /vmlinuz root=/dev/mapper/debian-vg-root ro quiet
```
but note something should appear in file `/etc/crypttab`, e.g.
```
cdisk0 UUID=12345678-9abc-def012345-6789abcdef01 none luks
```

LVM over LUKS for ArchLinux
---
> https://wiki.archlinux.org/index.php/Dm-crypt/Encrypting_an_entire_system  
> https://wiki.archlinux.org/index.php/Installation_guide  

Experiment performed on ArchLinux with Virtualbox.

* partition disk

GPT partition table
```
1mb-2mb bios_grub  -> sda1 (toggle bios_grub on)
2mb-256mb boot     -> sda2
256mb-100% luks    -> sda3
```

* make luks parts
```
cryptsetup luksFormat /dev/sda3
cryptsetup luksOpen /dev/sda3 luks
```

* setup lvm over luks
```
lvm pvcreate /dev/mapper/luks
lvm vgcreate lvm /dev/mapper/luks
lvm lvcreate -L 512M lvm -n swap
lvm lvcreate -l 100%FREE lvm -n root
```

* setup file system
```
mkfs.ext4 /dev/sda2
mkfs.ext4 /dev/mapper/lvm-root
mkswap /dev/mapper/lvm-swap
```

* mount for installation
```
mount /dev/mapper/lvm-root /mnt
swapon /dev/mapper/lvm-swap
mkdir /mnt/boot
mount /dev/sda2 /mnt/boot
```

* add hook in `/mnt/etc/mkinitcpio.conf`
```
HOOK=" ... encrypt lvm2 ... filesystems ... "
```

* install base system: edit `/etc/pacman.d/mirrorlist`
```
pacstrap /mnt base vim openssh
genfstab -p /mnt > /mnt/etc/fstab
vim /mnt/etc/hostname
arch-chroot /mnt
mkinitcpio -p linux # note: you should see [encrypt] and [lvm2] here, or it goes wrong.
systemctl enable dhcpcd@enp0s3.service
passwd
```

* install bootloader
```
grub-install --boot-directory=/mnt/boot/ /dev/sda
arch-chroot /mnt/
grub-mkconfig -o /boot/grub/grub.cfg
```
edit the config?
```
cryptdevice=UUID=<device_uuid>:lvm root=/dev/mapper/lvm-root
OR
cryptdevice=UUID=<device_uuid>:lvm root=UUID=<UUID>
```

* reboot

* post installation
```
pacman -Ss ecryptfs
pacman -S ecryptfs-utils
ecryptfs-setup-private || modprobe ecryptfs
ecryptfs-setup-private || modprobe ecryptfs
ecryptfs-mount-private
ecryptfs-umount-private
```

# LUKS Self-Destruction on Auth Failure for Debian

Just add your destruction code there.
```
Method 1: Via initramfs hook

dpkg -L cryptsetup
apt source cryptsetup

ack 'bad password'
 -> /usr/share/initramfs-tools/scripts/local-top/cryptroot

307         if [ ! -e "$NEWROOT" ]; then                                            
308             if ! crypttarget="$crypttarget" cryptsource="$cryptsource" \        
309                  $cryptkeyscript "$cryptkey" | $cryptopen; then                 
310                 message "cryptsetup: cryptsetup failed, bad password or options?"
311                 continue                                                        
312             fi                                                                  
313         fi  

update-initramfs -k all -u

e.g.

# Note, press Ctrl-v then Esc to input escape character ^[
message "^[[31;1m FATAL: triggered self-destruction process ..."
message "^[[33;1m  -> cryptsetup luksErase /dev/sda5"
#cryptsetup luksErase /dev/sda5 # It requires you to input uppercased 'YES'
# Certainly, you can change cryptsetup code to perform luksErase without asking.
message "^[[31;1m FATAL: self-destruction complete."
sleep 30

Method 2: change cryptsetup code

* cryptsetup commandline entrance src/cryptsetup.c

 @ 765 static int action_open_luks(void)

 815         r = crypt_activate_by_passphrase(cd, activated_name,                    
 816             opt_key_slot, NULL, 0, activate_flags);

* lib/setup.c

 @ 1983 int crypt_activate_by_passphrase(struct crypt_device *cd,

 2032     } else if (isLUKS(cd->type)) {                                              
 2033         /* provided passphrase, do not retry */                                 
 2034         if (passphrase) {                                                       
 2035             r = LUKS_open_key_with_hdr(keyslot, passphrase,                     
 2036                            passphrase_size, &cd->u.luks1.hdr, &vk, cd);         
 2037         } else                                                                  
 2038             r = volume_key_by_terminal_passphrase(cd, keyslot, &vk);            
 2039                                                                                 
 2040         if (r >= 0) {                                                           
 2041             keyslot = r;                                                        
 2042             if (name)                                                           
 2043                 r = LUKS1_activate(cd, name, vk, flags);                        
 2044         }                                                                       

 #2040: r>=0 means a valid key corresponding the given password is found.
        On password error, r should be -EPERM .

* lib/setup.c

 @ 973 int LUKS_open_key_with_hdr(int keyIndex,

  990     for(i = 0; i < LUKS_NUMKEYS; i++) {                                         
  991         r = LUKS_open_key(i, password, passwordLen, hdr, *vk, ctx);             
  992         if(r == 0)                                                              
  993             return i;                                                           
  994                                                                                 
  995         /* Do not retry for errors that are no -EPERM or -ENOENT,               
  996            former meaning password wrong, latter key slot inactive */           
  997         if ((r != -EPERM) && (r != -ENOENT))                                    
  998             return r;                                                           
  999     }                                                                           
 1000     /* Warning, early returns above */                                          
 1001     log_err(ctx, _("No key available with this passphrase.\n"));                
 1002     return -EPERM;

@ http://unix.stackexchange.com/questions/107739/how-to-trigger-a-system-self-destruct-with-a-certain-password-is-entered
@ https://github.com/offensive-security/cryptsetup-nuke-keys
```
