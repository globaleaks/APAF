"""
The basic apaf panel, accessible as it is from
"""
import os
import os.path
import sys

from twisted.internet import reactor
from twisted.web import server, resource, static
from twisted.python import log
from zope.interface import implements
from cyclone import web
import txtorcon

from apaf import hiddenservices
from apaf.core import Service, add_service
from apaf import config
from apaf.panel import handlers

class PanelService(Service):
    name = 'panel'
    desc = 'Administration panel and apaf manager.'
    port = 80
    icon = None

    _paneldir = os.path.join(config.services_dir, 'panel')
    handlers = [
        (r'/services/(.*)/start', handlers.ServiceHandler, {'action':'start'}),
        (r'/services/(.*)/stop', handlers.ServiceHandler, {'action':'stop'}),
        (r'/services/(.*)', handlers.ServiceHandler, {'action':'state'}),
        (r'/services', handlers.ServiceHandler),

        (r'/auth/login', handlers.AuthHandler, {'action':'login'}),
        (r'/auth/logout', handlers.AuthHandler, {'action':'logout'}),

        (r'/config', handlers.ConfigHandler),

#        (r'/tor', handlers.TorHandler),

        #(r'/(.*)', web.StaticFileHandler, {'path':config.static_dir}),
    ]

    def get_factory(self):
        # create the hidden service directory of the panel
        if not os.path.exists(self._paneldir):
            os.mkdir(self._paneldir)

        return web.Application(self.handlers, debug=True)

def start_panel(torconfig):
    """
    Set up the panel service, which lets the user customize apaf and choose
    which services are going to run.

    :param torconfig: an instance of txtorcon.TorConfig representing the
                      configuration file.
    """
    panel = PanelService()
    add_service(torconfig, panel)


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    start_panel()
    reactor.run()

