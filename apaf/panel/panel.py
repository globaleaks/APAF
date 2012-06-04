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
import txtorcon

from apaf import hiddenservices
from apaf.core import Service, add_service
from apaf.config import config
from apaf.panel import handlers

class PanelService(Service):

    name = 'panel'
    desc = 'Administration panel and apaf manager.'
    port = 80
    icon = None

    _paneldir = os.path.join(config.services_dir, 'panel')
    _api = dict(
        tor =  handlers.TorHandler,
        app =  handlers.AppHandler,
        status =  handlers.StatusHandler,
        service = handlers.ServiceHandler,
    )

    def onStart(self):
        self.root  = static.File
        root = static.File(config.static_dir)
        for path, handler in self._api.iteritems():
            root.putChild(path, handler())


        ## create the hidden service of the panel ##
        if not os.path.exists(self._paneldir):
            os.mkdir(self._paneldir)

        # listen on localhost :: XXX: shall be editable ::
        reactor.listenTCP(config.base_port, server.Site(root))

def start_panel(torconfig):
    """
    Set up the panel service, which lets the user customize apaf and choose
    which services are going to run.

    :param torconfig: an instance of txtorcon.TorConfig representing the
                      configuration file.
    """
    panel = PanelService()
    panel.onStart()

    add_service(torconfig, panel)

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    start_panel()
    reactor.run()

