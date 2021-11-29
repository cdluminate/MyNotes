This is a Title
===============
That has a paragraph about a main subject and is set when the '='
is at least the same length of the title itself.

Subject Subtitle
----------------
Subtitles are set with '-' and are required to have the same length 
of the subtitle itself, just like titles.

Lists can be unnumbered like:

 * Item Foo
 * Item Bar

Or automatically numbered:

 #. Item 1
 #. Item 2

Inline Markup
-------------
Words can have *emphasis in italics* or be **bold** and you can define
code samples with back quotes, like when you talk about a command: ``sudo`` 
gives you super user powers!

Insert a picture with ``.. image:: _static/system_activity.jpg``.

Themes
------

http://www.sphinx-doc.org/en/stable/theming.html

Math Support
------------

http://www.sphinx-doc.org/en/stable/ext/math.html

Add ``sphinx.ext.mathjax`` to your extension list in ``conf.py``, followed by
one extra new variable::

    mathjax_path = 'file:///usr/share/javascript/mathjax/MathJax.js?config=TeX-AMS-MML_HTMLorMML'
    #mathjax_path = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'

Example of inline math :math:`a^2+b^2=c^2` (Pythagoras).

Example of displayed math

.. math::

   \sin^2 (x) + \cos^2 (x) = 1

.. math:: E = mc^2
