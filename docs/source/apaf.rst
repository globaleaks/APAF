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

Threat Model
------------

*21:15 < rransom> What security properties should APAF provide? What attacks (or
classes of attacks) should APAF prevent or resist?*
This section describes the classes of attacks the APAF should prevent/resist.

Exposing to the net
    The APAF shall guarantee the **every** outgoing connection passes through tor.
    Incoming connections may be blocked if not coming from the tor network,
    depending on the configuration.
    Prevent XSSes?

Monkeypatch
    Other stdlibrary modules **must** be affected fom the monkeypatch.
    DNS leaking can be a problem. There is a huge number of functions using DNS
    queries: `socket.gethostbyname`, `socket.getaddrinfo`,
    `socket.gethostbyaddr`; probably are connected, take a look at the source.

Configuration
    Configuration files should never be accessible "as they are" from outside.
    The configuration shall be a python file, or a ConfigParser?

Authentication
    Web Framework are tested for this, should we trust them?

Core Library
------------

The core library consists in a set of monkeypatches to the satndard socket
library, making it bounce queries over the current tor proxy instance.


Configuration
-------------

The application can be customized using the browser. By default the
configuration page shall be accessible only from localhost, after authenticating
with a standard login form.
The restricted access of only localhost to the configuration section shall be
unckecked.

.. [#] : https://lists.torproject.org/pipermail/tor-dev/2012-March/003416.html
.. [#] : https://lists.torproject.org/pipermail/tor-dev/2012-April/003475.html



