## A long list of linux utilities

where `pkg` means `corresponding package in debian`  

APT/DPKG
---
1. `dpkg -L` lists package contents  
1. `dpkg -S` searchs to which package a file belongs  

Archive Utilities
---
1. `lsar` lists archive contents, pkg `unar`  
1. `unar` extracts contents from archive, pkg `unar`
1. `genisoimage` for generating iso files, pkg `genisoimage`, instead of `mkisofs`.  
2. `cdrecord`  
1. `rar`, `unrar`, `p7zip`, `p7zip-rar`  
1. `rename`  

note,
```
rename ’s/.rm$/.rmvb/’ *
rename ‘tr/A-Z/a-z/’ *
```

Debian specific
---
1. update-alternatives  

Terminal
---
1. `uxterm`  

> note, both `Ctrl^LeftClick` and `Ctrl^RightClick` will trigger menu.  
> note, change font with this:  
```
$ cat .Xdefaults
XTerm*faceName: Ubuntu Mono
XTerm*faceSize: 13
XTerm*background: black
XTerm*foreground: green
```
> note, download ubuntu font here `ubuntu/pool/main/u/ubuntu-font-family-sources/`  

> note, check `/etc/X11/app-defaults/XTerm`

2. `gnome-terminal`

3. guake

4. lilyterm

5. sakura

6. st (suckless.org)

System Monitoring
---
1. `conky`  
1. `dstat`  
1. `htop`  
1. kill all processes of user X `pkill -u X`

Disk information
---
1. hdparm  
2. blktool  
3. blkid  
4. lsblk  

Development
---
1. strace  
2. ltrace  
3. lsof  
4. fuser  
5. `update-java-alternatives`  

note
```
lsof -p PID
lsof somefile
lsof -i :PORT
```

Job Management
---
1. nohup  

PPPoE
---
1. pppoeconf  
2. pppd  

note,
```
pon dsl-provider
plog
poff [-a]
```

Networking
---
1. iproute2 package: ip ss iw  
2. netstat  
3. ifconfig  
4. iwconfig  
5. whois  
6. traceroute  
7. tracepath  

Downloading
---
1. wget  
2. axel  
3. lftp  

System service
---
1. systemctl  
2. /etc/init.d/SERVICE  
3. update-rc.d  

Change default shell
---
1. chsh  

Proxy
---
1. `export http_proxy=http://xx.xx.xx.xx:xxx`  

Text Processing
---
1. `fold -s txt` automatically wrap lines in your file
