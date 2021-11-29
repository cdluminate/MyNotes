Samba Service on Debian Server
==============================

Install the following packages with ``apt``:

1. ``samba`` for the server.
2. ``cifs-utils`` for the mount type cifs
2. ``smbclient``

usershare
---------
``/var/lib/samba/usershares``

add a user to sambashare group ``gpasswd sambashare -a USERNAME``

homeshare
---------

create a new samba user ``smbpasswd -a SAMBA_USER``

list users ``pdbedit -L -v``

change samba user password ``smbpasswd SAMBA_USER``

custom share
------------

before shareing a directory via samba service, make sure that the
permissions are correct.

::
  chown root:sambashare /destdir
  chmod 1770 /destdir

::
  [zfssmb]
  path = /luminz/smb
  available = yes
  browsable = yes
  public = no
  read only = no
  writeable = yes

Using samba service
------------------

list public shares ``smbclient -L hostname -U USERNAME``

mount a remote directory ``mount.cifs //server/sharename mountpoint -o user=USER,uid=USER,gid=GROUP,iocharset=utf8``

ZFS and samba
-------------
It does not matter whether you would turn on the ``sharesmb`` flag of a
ZFS to be shared or not. That flag is just for integration.

firewall
--------

``sudo ufw allow samba``

performance
-----------
::

  [global]
  server multi channel support = yes
  socket options = IPTOS_THROUGHPUT SO_KEEPALIVE
  deadtime = 30
  use sendfile = Yes
  write cache size = 262144
  min receivefile size = 16384
  aio read size = 16384
  aio write size = 16384
  load printers = no


reference
----
1. see also sshfs
2. https://wiki.samba.org/index.php/Main_Page
3. https://wiki.gentoo.org/wiki/Samba
4. https://wiki.archlinux.org/index.php/Samba
5. smb.conf

:Last-Update: 20180323
