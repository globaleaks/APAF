.. _utilities ::

Utility classes
================

Listed below are the most use(d|ful) object, and helper functions for starting
developing with apaf.

.. note: APAF is young, and keeps changing. What we are listing here is
         something directly related to the source code. And source code gets
         rewritten every day.

Services implementation
-----------------------
    Services are object exposing informations about how to set up themselves
    (via callbacks) and some extra metadata (via class attributes).

    .. autoclass :: apaf.core.IService
        :members:
    .. autoclass :: apaf.core.Service
        :members:


Configuration helper
---------------------
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
