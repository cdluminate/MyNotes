Grant someone access to the `sudo` command
===

Add this user to the `sudo` group

```
# adduser USER sudo
```

or modify `/etc/group` manualy.


`sudo` without password
===

Modify `/etc/sudoers` and and add this line, assuming the target user
name is USER.

```
USER ALL=(ALL) NOPASSWD: ALL
```
