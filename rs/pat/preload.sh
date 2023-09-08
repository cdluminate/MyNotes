#!/bin/bash
# This scripts will preload ILSVRC directory to memory
set -e
TARBALL=~/zfs/ILSVRC.tar
if test -e ILSVRC; then
	echo ILSVRC symlink already prepared.
else
	if ! test -e ${TARBALL}; then
		echo ${TARBALL} does not exist
	fi
	time tar xvf ${TARBALL} -C /dev/shm/
	ln -s /dev/shm/ILSVRC ILSVRC
	echo ILSVRC symlink is ready.
fi
