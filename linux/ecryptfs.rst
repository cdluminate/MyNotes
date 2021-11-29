ECryptfs Note
=============

Install ``ecryptfs-utils`` package.

To mount a ecryptfs directory
-----------------------------

see ``ecryptfs(7)``

::

    # mount -t ecryptfs [SRC DIR] [DST DIR]

Mount ~/Private directory
-------------------------

::

    $ ecryptfs-setup-private
    $ ecryptfs-mount-private
    $ ecryptfs-umount-private
