Vim
===

```
Ctrl^p    automatic completion

:Sex      split horizontally and browse the current directory
:Vex      similar

ggvG=     indent code automatically
```

# encrypt file

```
vim -x encrypted.txt
:help 'cm'
:setlocal cm=blowfish2
:wq
```

# remove non-ascii characters

```
set fileencoding=ansi
:wq
```
