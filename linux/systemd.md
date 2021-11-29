Systemd Notes
---
> systemd(1)
> Control systemd via : systemctl(1)

# status report in console

add kernel parameter
```
quiet                         --> kernel quiet, systemd quiet
quiet systemd.show_status=yes --> kernel quiet, systemd reports
```

# some threads about systemd in debian lists

https://lists.debian.org/debian-user/2014/03/threads.html
https://lists.debian.org/debian-user/2014/07/msg00180.html

# debian debate about init systems

https://wiki.debian.org/Debate/initsystem
https://wiki.debian.org/Debate/initsystem/systemd

# wiki

https://wiki.debian.org/systemd
https://wiki.archlinux.org/index.php/Systemd

hint:how to check kernel command line parameters/options ?
`cat /proc/cmdline`

# disabling services

if `systemctl disable toublemaker.service` doesn't prevent the service
in question from starting up. Try masking it with `systemctl mask trouble`.
The `mask` is the stronger version of `disable`. Systemd is bad!

# disable autodownload and autoinstall of packagekit

`systemctl mask packagekit`
`gsettings set org.gnome.software download-updates false`
