============
Dependencies
============
This sections explains the choices made for these tasks:

*  *Evaluate the currently available python networking frameworks and pick one*
*  *Evaluate the available python Tor Controllers and pick one*

Networking Framework
---------------------
Flask is probably the best choice, due to its popularity, its wide set of
plugins that can eventually extend the apaf itself, and the blueprint concept,
which is pretty safe in realtion to an administration page.

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
