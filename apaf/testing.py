""""
General-purpose utilities for testing.
"""

from twisted.web import client
from functools import partial, wraps

import txtorcon

import apaf
from apaf.panel import panel

class Page(object):
    """
    An asycnronous http client for fetching a predetermined handler.
    """

    def __init__(self, host='127.0.0.1', port=80):
        """
        Decorator helper for unittest.
        Uses asyncronous callbacks from twisted to get the page referred with path,
        and then tests it with the given path.
        :param host:    hostname of the appication. By default, `localhost`;
        :param port:    the port on which the application is listening
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
                    d.addCallback(partial(func, self)
                    ).addErrback(Page.std_errback)
                return d
            return wrap
        return inner

    @classmethod
    def std_errback(cls, exc):
        """
        Log the exception.
        """
        print exc

def start_mock_apaf(tor, *services):
    """
    Start the apaf for testing purposes.
    XXX. how to handle cleanup? Currently the reactor is left unclean
    :ret: None.
    """
    torconfig = txtorcon.TorConfig()

    ## start apaf. ##
    panel.start_panel(torconfig)

    for service in services:
            service = imp.load_module(
                      service, *imp.find_module(service, [config.services_dir])
                      ).ServiceDescriptor
    torconfig.HiddenServices = [x.hs for x in apaf.hiddenservices]
    torconfig.save()


    if tor:
        txtorcon.launch_tor(torconfig, reactor,
                            progress_updates=progress_updates,
                            tor_binary=config.tor_binary)
