.. _apaf:

===========================================
The Anonymous Python Application Framework
===========================================

The APAF aims to be an environment for python applcaition running on
hiddenservices, so that the developer, on one hand, can run its own twisted-based
web application also as hiddenservice, and on the other hand the final user can
have a great user experience.

Basic properties of the APAF were discussed and described on the tor-dev mailing
list [#]_ [#]_

Configuration
-------------

The application can be customized using the browser.
Specific platforms may have som graphic sugar, but the core remains an html
page, by default only accessible form localhost.

Packaging system
----------------

Packaging system responds to the need to have a single, portable executable for
running the application. But keep in mind that APAF can be run still as a standard python applciation. [installation.rst]

As packaging systems, we chose `py2app` for OSX builds,  `py2exe` for Windows
builds, and `python-stdeb` for Debian builds.

Mac OS X
........

Link to osx build.

Windows
.......

Link to windows build.

Linux
.....

Link to debian build.


.. [#] : https://lists.torproject.org/pipermail/tor-dev/2012-March/003416.html
.. [#] : https://lists.torproject.org/pipermail/tor-dev/2012-April/003475.html



