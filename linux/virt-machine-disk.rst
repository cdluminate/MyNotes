Disk images of virtual machines
===============================

::

  VBoxManage clonehd box-disk1.vmdk ubuntu.vdi --format vdi
  qemu-img convert -f vdi -O qcow2 ubuntu.vdi ubuntu.qcow2 
  qemu-img convert -f raw ubuntu.img -O qcow2 ubuntu.qcow2 
  VBoxManage convertdd ubuntu.img ubuntu.vdi 

::

  qemu-utils
  sudo modprobe nbd max_part=8
  qemu-nbd --connect=/dev/nbd0 xxx.qcow2
  qemu-nbd --disconnect /dev/nbd0

::

  when a disk image file takes much more space than actually
  used in the file systems:

  dd if=/dev/zero of=xxx
  then rm xxx to zero out the remaining space.
  qemu-img convert -O qcow2 orig.qcow2 trimmed.qcow2
