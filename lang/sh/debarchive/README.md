# DebArchive
  
[Tool] Simple Debian Source Syncer  
  
Download all Sources from the Debian Archive mirror site. Different from
debian mirroring scripts like `debmirror`, `DebArchive` syncs only source code.
  
### Usage
  
1. Specify your target mirror for `rsync` in config. e.g.:
```
SRC="xdlinux.info::debian/"
```
  
2. Just `make`
```
$ make
```

### Extra Funcion
  
1. [Statistic] Who is the most energetic dd ?
```
$ make who_is_the_most_energetic_dd
```
and this target would show your rank
```
$ make rank LOGIN=packages@qa.debian.org
```
where variable `LOGIN` stores your query, e.g. in above command line the `LOGIN`
is set to the Debian QA Team.  
  
If you want a full list, just type
```
$ make stat > txt
```

  
### License
```
BSD-2-Clause
```
