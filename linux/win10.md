Notes about installing windows 10
---

# windows update blocker

https://www.sordum.org/9470/windows-update-blocker-v1-2/

The mandatory updates from windows really suck a lot.

# disable services including windows update

Press `Win+R`, execute this command
```
service.msc
```
Then find the `Windows Update` service and disable it.

It is also recommened to disable HomeGroup-related services.

# remove junk components

launch powershell as superuser.
```
get-appxpackage | select packagefullname
get-appxpackage *windowsmap* | remove-appxpackage
dism /online /cleanup-image /analyzecomponentstore
dism /online /cleanup-image /startcomponentcleanup
```
Or use dism++: https://www.chuyu.me/en/index.html

# Advanced settings

Press `win+R`, and launch `mmc` via the popup window.
Add the management units which you would like to manipulate.

# ISO download

msdn.itellyou.cn
