Django integration
==================

Django integrations comes with the
`twisted.web.wsgi <http://twistedmatrix.com/documents/12.1.0/api/twisted.web.wsgi.html>`_
module.

TODO List
^^^^^^^^^

As you would do in any django project, create your database with: ::

    $ python manage.py syncdb

Remember to collect static file informations using: ::

    $ python manage.py collectstatic

This should create the ``static/`` directory in your root project. Remember to serve static files from inside twisted.



