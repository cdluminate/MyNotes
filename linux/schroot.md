Some schroot note
---

* clean up unused schroot session  
```
$ schroot -l -a
...
$ schroot -e -c <session>
```

```
[sid]
type=directory
profile=desktop
description=Debian sid (unstable)
directory=/home/debian/Sid
users=debian
groups=debian,sbuild
root-groups=root,debian
aliases=unstable,default
```
