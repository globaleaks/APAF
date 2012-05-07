============
Dependencies
============
This sections explains the choices made for these tasks:

*  *Evaluate the currently available python networking frameworks and pick one*
*  *Evaluate the available python Tor Controllers and pick one*

Networking Framework
---------------------
The decision to use `Twisted <http://twistedmatrix.com>`_ has been taken after a
discussion on IRC on the 6th of may on `#tor-dev`. Here the most important
motivations: ::

    Twisted is an event driven web framework, which not only supports multiple
    protocols, but despite its memory leaks and the weight of the library, it is
    widely used inside the tor community, hence maintenance and extendibility are
    worth its cons.

Tor Controller
--------------

*Personally, I am not sure whether a tor controller is really neeeded for the
application. Are we going to show statistics about the connection?*

Currently avaibles tor controllers are:
    - `TorCtl <https://gitweb.torproject.org/torctl.git/>`_ is pretty mature,
      even though its model IMHO is not really pythonic.
    - `Txtorcon <http://readthedocs.org/docs/txtorcon/en/latest/>`_ is a really
      cool controller, but brings with itself twisted libraries.
    - `Stem <https://gitweb.torproject.org/stem.git>`_ is immature, and the
      first version is going to be relased for this Summer of Code. But one of
      the developers, `atagar`, seems avaible for collaboration and focusing on
      the most critical parts.



Packing Everything
------------------

PyInstaller is probably the best choice if you want to build a single executable
of your application across multiple OSes. This implies a `hook/` directory in
the project tree.
