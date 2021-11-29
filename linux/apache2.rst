Launch a simple service via apache
==================================

install apache2
---------------

::

    $ sudo apt install apache2

configure
---------

then apache2 will autostart and systemd will enable it on boot by
default. Use sysv-rc-conf, or systemctl disable ... etc to disable it.

The configuration files are located at ``/etc/apache2``.

::

    apache2.conf -> the main configure file.
    `--ports.conf -> conf about ports.

Carefully read all config files under ``sites-enabled`` and edit them
according to your need.

check config and restart
------------------------

::

    $ sudo apachectl configtest
    $ sudo apachectl start # or systemctl start apache2

https with self-signed vertificate
----------------------------------

enable config

::

    $ sudo ln -s ../sites-available/default-ssl.conf . # sites-enabled

enable module

::

    $ sudo ln -s ../mods-available/ssl.conf . # mods-enabled
    $ sudo ln -s ../mods-available/ssl.load . # mods-enabled
    $ sudo ln -s ../mods-available/socache_shmcb.load . # mods-enabled

then restart service with ``systemctl restart apache2``. Note,
self-signed ssl certificate may cause warning from your browser.

reference
---------

Documentation at http://httpd.apache.org .
