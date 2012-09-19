.. APAF documentation master file


===========
About APAF
===========

APAF, aka Anonymous Python Application Framework, is a multi-platform *build system*
framework and a *library* for developing Python/Twisted based server applications,
exposed as Tor Hidden Service, easy to be installed and managed on multiple platforms
(Windows, OSX, Debian) with a particular focus for desktop environments.


Metadata
********
Author: Michele Orrù, aka maker


Project:  `Google Summer of code 2012 <http://code.google.com/soc/>`_


Further informations:

    * tor-dev mailing list:
        - project proposal  http://archives.seul.org/or/dev/Apr-2012/msg00031.html
        - status reports: http://archives.seul.org/or/dev/Jun-2012/msg00014.html
    * wikis and any other huge description of the apaf project


References
***********
 #. `Tor blog <https://blog.torproject.org/blog/gsoc-2012-projects>`_

 #. Any other site mentioning apaf


Features
********

**APAF** is a python library based on **twisted** and **txtorcon**. It can be
used for launching a standalone web application exposing itself via hidden
service, or as server application.

**Multiplatform**. APAF is tested on `Windows XP`, `Ubuntu 12.04` and `Mac OSX`.

**Portable**. Apart from the python package itself, APAF can be built as ``.app``,
using `py2app <http://svn.pythonmac.org/py2app/py2app/trunk/doc/index.html>`_,  and
``.exe``, using `py2exe <http://www.py2exe.org>`_ for windows.

**Easy**. exposing your application with APAF is as simple as writing a class
and 3 clicks (ehi, I am still working on this). A good starting point may be
the ``staticfileserver.py`` example.


**Secure** We make sure that all APAF's outbounding connecction will pass through Tor, and
that its fingerprint is reduced to a minimum.


.. warning:: we *do not guarantee* that the application built with APAF will not
            leak data outside tor, neither the same application will make APAF
            easily recognizable.
            The developer building applications with APAF should properly audit
            the applications they are packaging to check for possible leaks.

.. seealso:: See the threat model :ref:`page <threat_model>` for further
             informations.


Installation
************

APAF can be installed using either ``pip`` or ``easy_install``.
There should be somewhere also builds for debian. ::

$ pip install git+https://github.com/globaleaks/APAF.git



Running
*******
To try out apaf, just run: ::

$ python apaf/main.py

In case you are not interested in user-experience and similar bullshits, ``--debug`` option could be helpful.


Coding
******

Follows below the table of libraries.

.. toctree::
   :maxdepth: 2

   apaf-package
   threat_model
   build_osx
   build_debian
   build_win32


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* `The Tor Project`__

__ torproject_

.. _torproject: https://www.torproject.org
