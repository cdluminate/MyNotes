Connman Tips
============

https://wiki.archlinux.org/index.php/ConnMan

QT Gui: cmst

# Enable wifi

connmanctl
> technologies
> enable wifi
> disable wifi

connmanctl
> scan wifi
> services
> connect wifi_dc85de828967_4d6568657272696e_managed_none

connmanctl
> scan wifi
> services
> agent on
> connect wifi_dc85de828967_4d6568657272696e_managed_none

> quit
