.. _utilities ::

Utility classes
================

.. note: APAF is young, and keeps changing. What we are listing here is
         something directly related to the source code. And source code gets
         rewritten every day.

If you are a web application developer interested in using APAF for exposing its
application to the dark net with a .onion domain, that's the right place for
you.

APAF communicates with external application using the class `apaf.core.Service`,
which exports some metadata such as name `apaf.core.Service.name`, descirption
`apaf.core.Service.desc`, exc.; serves the twisted's factory class
`twisted.internet.protocol.factory`; and has its own configuration file in yaml
syntax.


At the bottom of this document you will see some informations about also
`apaf.testing` module. It is supposed to be used from each new application
inside its ```test/``` directory.


Services implementation
-----------------------
Services are object exposing informations about how they need to be set up
(callbacks), their metadata (class attributes) and user configuration
(service.config static attribute)

    .. autoclass :: apaf.core.IService
        :members:
    .. autoclass :: apaf.core.Service
        :members:


Configuration helper
---------------------
Each `apaf.core.Service` class has its `apaf.config.Config` instance, which
interfaces to pyYaml for provinding a simple configuration file, writted in
a human-readable format such is yaml and organized with default fields.

    .. autoclass :: apaf.config.Config
        :members:


Testing
-------

Cyclone, unlike tornado, does not provide any testing module. APAF tries to meet
unit testing needs providing :py:mod:`apaf.testing`.
In this module you will find some decorators and some helper functions.

Decorators
**********
    .. py:decorator :: apaf.testing.Page
    .. py:decorator :: apaf.testing.json


Functions
*********
    .. py:function :: apaf.testing.start_mock_apaf
