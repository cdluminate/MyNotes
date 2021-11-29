SATA disk hotplugging
===

Platform:

1. ASUS Z10PE-D8 WS.

2. A failed Seagate drive in a ZFS pool.

# Remove a disk physically, and add a new one

* locate the disk, both logically (e.g. `/dev/sdb`) and phisically
(e.g. which hard disk fails).

```
$ ls /dev/disk/by-id/ -l
$ sudo dmesg | grep sdb
[    2.964600] sd 1:0:0:0: [sdb] Attached SCSI disk
```

* make sure that the disk to be removed is working under AHCI mode.
According to ArchWiki, one of the advantages of ACHI is hotpluggable.

> https://wiki.archlinux.org/index.php/AHCI

```
$ sudo dmesg | grep scsi           1741ms < Mon 27 Mar 2017 05:28:44 AM UTC
[    1.858058] scsi host0: ahci
[    1.858504] scsi host1: ahci
...
```

* umount all filesystems and all processes related to that drive.

* delte this drive from the kernel.

```
echo 1 > /sys/bus/scsi/devices/<n>:0:0:0/delete
```

* unplug that drive from the motherboard.

* plug a new disk there

* trigger a kernel re-scan?

```
echo "0 0 0" >/sys/class/scsi_host/host<n>/scan
```

## reference

http://fredericiana.com/2010/06/15/hot-plugging-a-sata-drive-under-linux/

https://www.codeproject.com/articles/460058/sata-hotplug-add-remove-sata-hdd-in-a-jiffy

https://wiki.archlinux.org/index.php/AHCI
