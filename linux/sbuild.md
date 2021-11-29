Debian's sbuild
===

sudo sbuild-adduser myself sbuild

newgrp

sudo sbuild-createchroot --include=eatmydata unstable /srv/chroot/unstable-amd64-sbuild https://mirrors6.tuna.tsinghua.edu.cn/debian/

sbuild -d unstable xyz.dsc

sudo sbuild-udpate -udcar unstable-amd64-sbuild

sudo sbuild-shell source:unstable-amd64-build
(for updating sources.list)

https://wiki.debian.org/sbuild

autopkgtest
```
$external_commands = {
  'post-build-commands' => [
    [
      'autopkgtest', '%d', '%c',
      '--', 'schroot', 'unstable-%a-sbuild;',

      # if autopkgtest's exit code is 8 then the package had no tests
      # but this isn't a failure, so catch it
      'aptexit=$?;',
      'if', 'test', '$aptexit', '=', '8;', 'then',
      'exit', '0;', 'else', 'exit', '$aptexit;', 'fi'
    ],
  ],
};
```

build package in experimental

```
sbuild -d unstable -j4 --extra-repository='deb http://deb.debian.org/debian experimental main' --no-arch-all --arch-any --no-source opencv_3.4.4+dfsg-1~exp1.dsc
```
