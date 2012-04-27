.. _apaf:

===========================================
The Anonymous Python Application Framework
===========================================

This sections explais the choices meade for these tasks:
*Define what the threat model for APAF is and what sort of properties it should provide*


The APAF project aims to be a static file server written in python, on the same
development idea behind the tor browser bundle: being a simple and
portable executable for non-technical users. [#]_

Basic properties of the APAF are well-described by Arturo Filastò on the tor-dev
mailing list. [#]_ The core model consists in a basic library which interfaces
with tor, and a basic application server.


Core Library
------------

The core library consists in a set of monkeypatches to the satndard socket
library, making it bounce queries over the current tor proxy instance.


Configuration
-------------

*Customizing the application and tor setup can be done wither via web interface
or a simple GUI.*


.. [#] : https://lists.torproject.org/pipermail/tor-dev/2012-March/003416.html
.. [#] : https://lists.torproject.org/pipermail/tor-dev/2012-April/003475.html



