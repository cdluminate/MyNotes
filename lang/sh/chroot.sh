#!/bin/sh
set -e -x

CHROOT='Gitlab'

echo "chroot into $CHROOT"

mount --bind /proc proc
mount --bind /sys sys
mount --bind /dev dev

echo " -> Run /opt/gitlab/embedded/bin/runsvdir-start in background."
echo " -> Start gitlab with «gitlab-ctl start»."
echo " ->  Work with Gitlab."
echo " -> Stop gitlab with «gitlab-ctl stop»."

chroot . /bin/bash

umount -R proc
umount -R sys
umount -R dev
