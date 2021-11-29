Inspecting SMART attributes of hard drives
===

First install package in need,
```
$ apt install smartmontools            # Debian/Ubuntu
$ pacman -S smartmontools              # ArchLinux
```

then check your disk status with
```
$ smartctl -HcA /dev/sda
$ smartctl -a /dev/sda
$ smartctl -x /dev/sda
```

perform disk self-test
```
$ smartctl -t short /dev/sda
```

Sometimes we need to read smart attributes from disks
hooked onto RAID card
```
$ sudo smartctl --scan
/dev/sda -d scsi # /dev/sda, SCSI device
/dev/sdb -d scsi # /dev/sdb, SCSI device
/dev/sdc -d scsi # /dev/sdc, SCSI device
/dev/bus/0 -d megaraid,0 # /dev/bus/0 [megaraid_disk_00], SCSI device
/dev/bus/0 -d megaraid,1 # /dev/bus/0 [megaraid_disk_01], SCSI device
/dev/bus/0 -d megaraid,2 # /dev/bus/0 [megaraid_disk_02], SCSI device

$ smartctl -d megaraid,0 /dev/bus/0 -a
```

## reference

man smartctl
