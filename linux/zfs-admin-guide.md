Notes on Solaris ZFS Administration Guide
===

> Sun, Solaris ZFS Administration Guide, Jan.2010  

# Getting Started

## Create ZFS storage pool

zpool

## Create ZFS file system hierarchy

zfs

# ZFS and traditional filesystem differences

pass

# Managing storage pool

1. Physical storage can be any block device of at least 128 MBytes in size.  
2. The recommended mode of operation is to use an entire disk. ZFS formats the disk using EFI labels.  

Note, ZFS root pool must be created with an SMI (VTOC) label instead of an EFI label.  

# Installing and Booting a ZFS root filesystem

# Managing zfs file systems

inheriting ZFS properties.
```
# zfs inherit -r compression tank/home
```

remount as read-only
```
# zfs mount -o remount,ro tank/home
```

# Working with ZFS snapshots and clones

# Using ACLs and attributes to protect ZFS files

# ZFS delegated administration

# ZFS Advanced topics

# ZFS troubleshooting and recovery

..

Marked as done, 4 sept 2016
