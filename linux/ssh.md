SSH Notes
===

SSH use password first
----------------------

```
ssh -pPORT user@host -o PreferredAuthentications=password
```

SFTP chroot
-----------
https://wiki.archlinux.org/index.php/SFTP_chroot

SSH could not load host key
---
```shell
ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key
ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key
ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key

OR SIMPLY

ssh-keygen -A
```

SSH over SCTP
-------------

Server side: `socat sctp-listen:2222,fork tcp:localhost:22`
Client side: `socat tcp-listen:2222,fork sctp:servier:2222`

In this way setting up a socks5 tunnel is also possible:
`ssh -lusername localhost -D 8080 -p 1337`
