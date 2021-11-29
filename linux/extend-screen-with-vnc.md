Extending Screen with VNC Server
===

> https://unix.stackexchange.com/questions/156412/vnc-server-as-a-virtual-x11-monitor-to-expand-screen

> https://bbs.archlinux.org/viewtopic.php?id=191555

> https://wiki.archlinux.org/index.php/TigerVNC

> https://wiki.archlinux.org/index.php/X11vnc

> https://wiki.archlinux.org/index.php/Xrandr

## Install required packages

`x11vnc` `tightvncserver` `xtightvncviewer` `xrandr` `arandr`

## Extending

* Check the current output. Pick an unused output from `xrandr`. E.g. `DP-1`.

* Generate a mode with `cvt 1600 900` or `gtf 1600 900 60` where `1600x900` is the resolution of your secondary screen. E.g. `"1600x900_60.00"  119.00  1600 1696 1864 2128  900 901 904 932  -HSync +Vsync`

* Add the mode to xrandr like this `xrandr --newmode "1600x900_60.00"  119.00  1600 1696 1864 2128  900 901 904 932  -HSync +Vsync`

* Put the unused output, e.g. `DP-1` in that mode.

```
xrandr --addmode DP-1 1600x900_60.00
xrandr --output DP-1 --mode 1600x900_60.00 --left-of LVDS-1
```

* Export that output with x11vnc, choosing an appropriate offset.

```
x11vnc -clip 1600x900+0+0 -passwd PASSWD -speeds lan -nowf -nowcr
```

* Connect from the client

```
vncviewer -fullscreen 192.168.1.1::5900 
```

* Close the output

```
xrandr --output DP-1 --off
```

## Sidenote

When you need to rotate an output,
```
xrandr --output HDMI-1 --rotate left
```
available rotations are `left`, `right`, `normal` and `invert`.
See man xrandr for more detail.

## Trouble and tips

* `ctrc` failure: select another unused output and try again.

* Press F8 to pop up a menu in vncclient

* use `xrandr --output DVI-0 --primary` to move your pannel.

* You can use any device to extend your screen as long as it has vnc client, and
is able to connect your computer and x11vnc server. For example, Another linux
laptop is applicable, when it has any vnc viewer. An Android phone is applicable
too, all that you need is to install an vnc viewer on your phone.

* `-[no]wf` for wireframe

```
x11vnc -clip 2048x1536+0+0 -passwd asdf -cursor most -wf -nowcr -viewonly -cursor most -speeds modem
```
