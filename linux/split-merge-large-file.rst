Splitting and Merging large files
=================================

Ref: https://unix.stackexchange.com/questions/1588/break-a-large-file-into-smaller-pieces

splitting
---------

.. code::

  $ split -b 500m my-large-file prefix

  $ cat prefix* > my-restored-large-file
