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
The `Txtorcon <http://readthedocs.org/docs/txtorcon/en/latest/>`_ is a really
cool controller based on twisted. Even though it is not considered mature, it
acts on the same framework we are going to use, hence is probably the best
choice for interfacing with a new tor process.


Packing Everything
------------------

PyInstaller is probably the best choice if you want to build a single executable
of your application across multiple OSes. This implies a `hook/` directory in
the project tree.


.. note ::
    pyInstaller wont' provide any 64 bit version for osx.


The latest stable of pyInstaller seems to do not have any hooks-twisted.py.
Anyway an echo server has been built without too many problems on my
machine. [1]_



.. [1] this was tested on osx with pyInstaller 1.5.1 and python2.7. Note that
         anyway the final executable was not working.
