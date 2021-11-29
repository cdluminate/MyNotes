Extend ext4 partition on a GPT-scheme disk
===

## assumption

```
SCSI disk /dev/sda

partition  start  end   type
/dev/sda1  10GB   20GB  ext4
/dev/sda2  20GB   30GB  any
/dev/sda3  40GB   100%  any
```

Assume that `/dev/sda2` is deprecated, and we want to
extend the size for the ext4 filesystem on `/dev/sda1`.

This way only works for the partitions that are continuous
in physical address.

#### 1. delete `/dev/sda2` in GPT

```
parted /dev/sda
rm <id_of_sda2>
resizepart <id_of_sda1> 30GB
```

then from the view of GPT record, `/dev/sda1` is extended
to `20GB` (end - start = size) now. However we also need
to resize the filesystem itself, apart from the GPT partition.

#### 1.1 check result

```
lsblk
```

You can see your `/dev/sda1` is currently 20GB.

```
df -h
```

However `df` gives you an different answer, which
indicates that the ext4 filesystem has not been resized yet.

#### 2. resize `ext4` filesystem

```
resize2fs /dev/sda1
```

Yes, the default action is to adjust filesystem size according
to the partition information. Note, what is awesome, online resize is supported!

#### 2.1 check result

```
lsblk
df -h
```

Now you your `/dev/sda1` gets 20GB without pain.
