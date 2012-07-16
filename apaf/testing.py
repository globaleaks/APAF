""""
General-purpose utilities for testing.
"""

from twisted.web import client
from functools import partial, wraps

class Page(object):
    def __init__(self, host, port):
        """
        Decorator helper for unittest.
        Uses asyncronous callbacks from twisted to get the page referred with path,
        and then tests it with the given path.
        """
        self.host = host
        self.port = port

    def __call__(self, path, raises=False, **settings):
        url =  'http://%s:%d%s' % (self.host, self.port, path)

        def inner(func):
            @wraps(func)
            def wrap(self):
                d = client.getPage(url, **settings)
                if raises:
                    d.addErrback(partial(func, self))
                else:
                    d.addCallback(partial(func, self))
                return d
            return wrap
        return inner

