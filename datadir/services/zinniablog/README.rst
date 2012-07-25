Django integration
==================

Django integrations comes with the
`twisted.web.wsgi <http://twistedmatrix.com/documents/12.1.0/api/twisted.web.wsgi.html>`_
module.

Note> remember to collect static file informations using: ::

$ python manage.py collectstatic

This should create the ``static/`` directory in your root project. Remember to serve static files from inside twisted.



