Xorg+Dwm notes
===

# failed to start dwm with `startx`, but `sudo startx` works

Machine: Virtualbox 5.1.14
OS: Debian Sid / 20170204

The error message looks like this
```
failed to set IOPL for I/O (Operation not permitted)
```

See Debian bug `Bug#802327`. The solution is to install the
`xserver-xorg-legacy` package.

# Fixing misbehaving Java applications

> https://wiki.archlinux.org/index.php/Dwm

```
export _JAVA_AWT_WM_NONREPARENTING=1
```
