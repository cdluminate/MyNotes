# 1: original
$ gsettings set org.gnome.desktop.interface scaling-factor 1
# 2: 2x
$ gsettings set org.gnome.desktop.interface scaling-factor 2

# 24: default cursor size
$ gsettings set org.gnome.desktop.interface cursor-size 24
# 64: really big cursor
$ gsettings set org.gnome.desktop.interface cursor-size 64
# another way to change cursor size
$ dconf write /org/gnome/desktop/interface/cursor-size 48

# https://wiki.archlinux.org/index.php/Cursor_themes
