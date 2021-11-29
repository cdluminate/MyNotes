Tips about Debian Development
=============================

merging two .changes file
-------------------------

.. code::

   mergechanges -f intel-mkl_xxx_amd64.changes intel_mkl_xxx_i386.changes
   changestool intel-mkl_xxx_multi.changes updatechecksums
   debsign -k yyy intel-mkl_xxx_multi.changes
