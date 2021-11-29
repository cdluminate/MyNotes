Btrfs
===

> https://wiki.archlinux.org/index.php/Btrfs#Known_issues  
> http://www.funtoo.org/BTRFS_Fun  

> https://btrfs.wiki.kernel.org/index.php/Getting_started  
> https://btrfs.wiki.kernel.org/index.php/Getting_started#Basic_Filesystem_Commands  
> https://wiki.archlinux.org/index.php/Btrfs  
> https://btrfs.wiki.kernel.org/index.php/Main_Page  

OpenSUSE use Btrfs as its default file system at least on OpenSUSE Leap 42.

## btrfs

Create filesystem on a single device `mkfs.btrfs -L mylabel /dev/sdb1`

Show btrfs filesystems `btrfs filesystem show`

Mount btrfs filesystem `mount /dev/sdb1 /mnt`

Create subvolume `btrfs subv create /mnt/test`

List subvolume `btrfs subv list /mnt`

Delete subvolume `btrfs subv delete /mnt/junk`

Filesystem usage `btrfs filesystem df /mnt`, `btrfs filesystem usage /mnt`

Scrub device `btrfs scrub start /mnt`

Scrub status `btrfs scrub status /mnt`

Create snapshot `btrfs subv snap /mnt /mnt/.btrfs/snap1`

Send snapshot `btrfs send /root_backup | btrfs receive /backup`

## snapper

> https://wiki.archlinux.org/index.php/Snapper  

`sudo apt install snapper`

Create snapper config `snapper -c bt create-config /mnt`

List snapper snapshots `snapper -c bt list`

Create snapshot `snapper -c bt create -d "before cleanup"`

Compare snapshots `snapper -c bt status 1..2`

Show file differences between snapshots `snapper -c bt diff 1..2`

