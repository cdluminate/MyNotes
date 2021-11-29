RST Note
========

Sample paragraph one.

  Indented sample paragraph two. This is block quotes too.

Paragraph three.

Section title
-------------

Subsection title
~~~~~~~~~~~~~~~~

Text Style
----------

Inline markups:

  *italics*

  **bold**

  ``fixed-space literal string``

Lists
-----

1. numbers style 1

#. auto-enumerated

(1) numbers style 2

1) numbers style 3

A. upper-case letters.
   sample text.

a. lower-case letters

* bullet

  - sub-list

    + sub-sub-list

  - another sub-list

what
  definition list

*how*
  sample text

Code Samples
------------

an example::

  import sys

::

  literal block example

Field Lists
-----------

:Authors: foobar
:Version: alpha
:Date:    2017
:Tag:     abc

Tables
------

Simple table:

====== ==========
Input  Output
------ ----------
1      1
2      4
3      9
====== ==========

Others
------

Images.

Reference
---------

reference: [1]_ [2]_

auto-numbered [#]_ [#]_

citation [cite1]_

hyperlink example Python_

`phrase reference`_

|reST| replacement text

.. [1] A ReStructuredText Primer

.. [2] http://docutils.sourceforge.net/docs/user/rst/quickref.html

.. [#] foobar 1

.. [#] foobar 2

.. [cite1] citation 1

.. _Python: https://python.org

.. |reST| replace:: reStructuredText
