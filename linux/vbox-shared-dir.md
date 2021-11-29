VBox shared directory
===

> reference: Oracle VM Virtualbox User Manual  

> file: /usr/share/doc/virtualbox/UserManual.pdf   

> https://wiki.archlinux.org/index.php/VirtualBox#Enable_shared_folders

> package: virtualbox

### install guest addition

1: via guest addition cdrom
```
cd /media/cdrom
./VBoxXXX.run
```
make sure you already have `gcc` `make` `dkms` and `linux-headers` installed on the guest system.

2: debian package
```
apt install virtualbox-guest-dkms virtualbox-guest-utils
```

### manual mount

1: windows guest, manual mount
```
net use x: \\vboxsvr\sharename
```
or mapping a network device to "My Computer".

2: linux guest, manual mount
```
VBoxControl sharedfolder list #> list available shared folders
mount -t vboxsf sharename mountpoint
```

### auto mount

1: linux guest
```
reboot
cd /media/sf_sharename #> auto-mounted here, with name prefixed by 'sf-'
```

2: windows.  ...  
