OpenBSD notes
---

> some books http://www.openbsd.org/books.html

> general documents including installation guide http://www.openbsd.org/faq/index.html

## install with install59.iso

On first boot please check mail.

GPT may not boot for 5.9 .

## Packages and ports

* Packages

```
pkg_add(1)    - a utility for installing and upgrading software packages
pkg_delete(1) - a utility for deleting previously installed software packages
pkg_info(1)   - a utility for displaying information about software packages
pkg_create(1) - a utility for creating software packages
```

to install vim, add this line to profile, then source profile
```
export PKG_PATH=http://a.local.mirror/$(uname -r)/packages/$(uname -m)/
```
then
```
pkg_add vim
```

list installed packges
```
pkg_info
```

update installed package
```
pkg_add -u vim
```

* Ports

based on Makefile
