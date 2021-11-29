Keyboard Settings
=================

see https://wiki.archlinux.org/index.php/Keyboard_configuration_in_console  

Apple Keyboard
--------------

https://unix.stackexchange.com/questions/121395/on-an-apple-keyboard-under-linux-how-do-i-make-the-function-keys-work-without-t

How to change keyboard behaviour so that F1--Fn works without pressing
the Fn key?

```
echo 2 > /sys/module/hid_apple/parameters/fnmode

where 1 = fkeyslast
      2 = fkeysfirst
```

to make this change persistent, add this to `/etc/modprobe.d/hid_apple.conf` and
re-generate the initramfs.

```
options hid_aple
```

keyboard layout
---------------

::

  $ localectl set-keymap us us
  $ localectl set-x11-keymap de

::

  setxkbmap -layout us,de
  setxkbmap -print -verbose 10

TTY font
--------

::

  sudo dpkg-reconfigure console-setup

TTY typematic delay and rate
----------------------------

::

  kbdrate -d <delay> -r <rate>

  kbdrate -d 1 -r 60

``/etc/systemd/system/kbdrate.service``

::

  [Unit]
  Description=Keyboard repeat rate in tty.
  
  [Service]
  Type=simple
  RemainAfterExit=yes
  StandardInput=tty
  StandardOutput=tty
  ExecStart=/usr/bin/kbdrate -s -d 450 -r 60
   
  [Install]
  WantedBy=multi-user.target

Xorg typematic latency and repeat rate
--------------------------------------

::

  xset r rate 160 160

Input greek letters
-------------------

method 1: fcitx + googlepinyin

1. instsall package ``fcitx`` and ``fcitx-googlepinyin``
2. switch to pinyin mode, then type `;\alpha`, then type space.
   symbol α will be produced.

method 2: hardcode

https://newton.cx/~peter/2013/04/typing-greek-letters-easily-on-linux/  

1. type `Ctrl+Shift+u 0 3 c 3 <space>` for σ  

Compose keys (XCompose)
-----------------------

https://unix.stackexchange.com/questions/229555/how-do-i-unset-an-option-in-xkbmap
https://askubuntu.com/questions/451945/permanently-set-keyboard-layout-options-with-setxkbmap-in-gnome-unity
http://duncanlock.net/blog/2013/05/03/how-to-set-your-compose-key-on-xfce-xubuntu-lxde-linux/

::

  /etc/default/keyboard
  XKBOPTIONS="compose:ralt"

  or setxkbmap -option compose:ralt  # immediately
  ref: /usr/share/X11/xkb/rules/xorg.lst

When X's keybinding Shift+Alt is conflicting with your xbindkeys::

  setxkbmap -option "grp:shift_caps_toggle"  # this is root of problem
  setxkbmap -option "grp:alt_shift_toggle"   # better

To remove options from setxkbmap, e.g.::

  setxkbmap -option -option ""
  setxkbmap -option -option compose:caps  # override all other compose keys
  setxkbmap -option -symbols "pc+us+us:2+inet(evdev)+compose(caps)"  # override xkb_symbols
  

Natural Scrolling of Touchpad
-----------------------------

https://askubuntu.com/questions/91426/reverse-two-finger-scroll-direction-natural-scrolling

::

  xinput list
  xinput list-props {device ID}
  e.g. xinput list-props 15
  xinput set-prop {device ID} {property NUM} value1 value2 value3 ...
  e.g. xinput set-prop 15 312 -114 -114
