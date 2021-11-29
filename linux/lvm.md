LVM on linux
---
> linux.vbrid.org  
> software package `lvm2`.  
> https://wiki.archlinux.org/index.php/LVM  

## Physical Volumes  

0. prepare partitions with tools e.g. `parted`. Don't forget to toggle the lvm flag.  

1. `pvscan` to scan for physical volumes.   

2. create pv with `pvcreate`, e.g. `pvcreate /dev/sdc1`.  

3. use `pvscan` can `pvdisplay` to check the result.  

## Volume Groups  

1. create volume group with `vgcreate -s 8m luminvg /dev/sdc{1,2}`.  

2. `vgscan`, `pvscan`, `vgdisplay`.  

3. assign more physical volume to volume group with `vgextend luminvg /dev/sdc3`.  

## Logical Volumes  

1. create lv with `lvcreate -L 2G -n luminlv luminvg`.  

2. `lvscan`, `lvdisplay`.  

## Filesystem  

1. make a file system on virtual device `mkfs.ext4 /dev/luminvg/luminlv`.  

2. `mount /dev/luminvg/luminlv /mnt`  

3. enjoy this filesystem!  

## Modifications on LV: Enlarge your LV  

1. `lvm vgs`, you find that there is still free space available.  

2. `sudo lvm lvresize -L +500m /dev/luminvg/luminlv`  

3. resize your filesystem with `sudo resize2fs /dev/luminvg/luminlv`.  

#### Shrink ext4 filesystem then shrink LV

1. `sudo lvreduce --resizefs -L -30m /dev/luminvg/luminlv`  

#### add some space back

1. `sudo lvm lvresize --resizefs -L +500m /dev/luminvg/luminlv`  

## Remove lVM  

1. umount your filesystem  

2. remove LV with `sudo lvm lvremove luminvg/luminlv`  

3. set volume group inactive `sudo lvm vgchange -a n luminvg`  

4. remove VG `sudo lvm vgremove luminvg`  

5. remove PV `sudo lvm pvremove /dev/sdc{1,2,3}`  

lumin, 05 May 2016
