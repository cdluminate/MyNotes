Wine on Debian
---

wine on i386 is fine. `apt install wine32`.

For amd64 architecture the user need to add multi-arch first:
```
# dpkg  --add-architecture i386  // set up multi-arch  
# apt-get update
# apt-get install wine:i386
```

How to force winetricks use a 32-bit wineprefix?
---

```
rm -rf ~/.wine
WINEARCH=win32 winetricks --gui
```

Chiense Character turns to be unreadable blocks
---

```
LC_ALL=zh_CN.utf-8 wine PROGRAM
```
