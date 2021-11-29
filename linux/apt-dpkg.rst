APT and DPKG tricks
===================

Backup and restore package selections with apt/dpkg
---------------------------------------------------

Backup package list:

.. code:: shell

    # dpkg --get-selections > pkg.list

Restore:

.. code:: shell

    # dpkg --set-selections < pkg.list
    # apt-get -u dselect-upgrade # this will pull and install all missing packages

see dpkg(1)

Sources.list
------------

.. code:: shell

    # To add an CD-ROM, use apt-cdrom

    deb file:///debian jessie main contrib non-free

    deb http://ftp.cn.debian.org/debian jessie main contrib non-free
    deb http://ftp.cn.debian.org/debian jessie-backports main contrib non-free
    deb http://ftp.cn.debian.org/debian jessie-proposed-updates main contrib non-free
    deb http://ftp.cn.debian.org/debian-security jessie/updates main contrib
    deb http://ftp.cn.debian.org/debian unstable main contrib non-free
    deb http://ftp.cn.debian.org/debian experimental main contrib non-free

    deb-src http://ftp.cn.debian.org/debian jessie main contrib non-free
    deb-src http://ftp.cn.debian.org/debian unstable main contrib non-free

    deb http://ftp.cn.debian.org/debian jessie main contrib non-free
    deb-src http://ftp.cn.debian.org/debian jessie main

APT preferences
---------------

see ``apt_preferences (5)``

List and Search package contents
--------------------------------

.. code:: shell

    $ dpkg -S pkg  # to search installed package content
    $ dpkg -L pkg  # to list installed package content
    $ apt-file sesarch file  # search file among both installed and uninstalled packages

Package dependency
------------------

.. code:: shell

    $ apt-cache depends pkg
    $ apt-cache rdepends pkg

    # aptitude can resolve some tough dependency situation
    $ aptitude install pkg-with-dependency-trouble

Purge packages that are not completely removed
----------------------------------------------

::

    $ dpkg -l | grep ^rc | awk '{print $2}' | sudo xargs dpkg --purge

Speedup APT
-----------

.. code::

   $ dpkg-divert --divert /usr/bin/apt.real --rename /usr/bin/apt
   $ cat /usr/bin/apt
   #!/bin/sh
   eatmydata -- apt.real $@

For more information see ``dpkg-divert(1)`` and ``eatmydata(?)``.
