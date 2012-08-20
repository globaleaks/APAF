File System Structure
=====================

APAF comes with a very simple `file system structure`. ::

     - apaf/
       |- test/
     - datadir/
       |- contrib/
       |- config/
       |- services/
     - docs/

Apart from the standard package directory ``apaf/`` , which will be covered
further in :ref:`APAF utilities <utilities>`, and ``docs/`` that is the
directory you are currently reading from, ``datadir`` contains
everything for building a new apaf :class:`apaf.core.Service`.

``contrib/`` holds every bundles binary provided with the final application. If
you are going to use external binary tools, you can place them here and access
afterwarss via ``apaf.config.binary_kits``

``config/`` contains every configuration file previously created with
:class:`apaf.config.Config`.

``services/`` is the root directory for external services. By default, it
contains some examples, but feel free to change those :D.


