Reprepro notes
===

`conf/distributions`

```
Origin: Debian
Label: SIMDebian
Suite: unstable
Codename: sid
Version: 10.0
Architectures: source amd64
Components: main non-free contrib
Description: SIMDebian
```

```
reprepro -Vb. list unstable
reprepro -Vb. list sid
reprepro -Vb . include unstable ../dpkg.pkg/dpkg_1.19.4+haswell1_amd64.changes
reprepro -Vb ../archive/ include sid dpkg_1.19.4+haswell1_source.changes
reprepro -A amd64 -Vb /srv/simdebian/public/nehalem include unstable *.changes
```
