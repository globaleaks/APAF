"""
The basic apaf panel, accessible as it is from
"""
import os
import os.path
import sys

from twisted.internet import reactor
from twisted.web import server, resource, static
from twisted.python import log
import txtorcon

from apaf import hiddenservices
from apaf.config import config
from apaf.panel import handlers

PANEL_DIR = os.path.join(config.tor_data, 'panel')
STATIC_DIR = os.path.join('apaf', 'panel', 'static')

API = {
    'tor': handlers.TorHandler,
    'app': handlers.AppHandler,
    'status': handlers.StatusHandler
}

def start_panel(torconfig):
    """
    Set up the panel service, which lets the user customize apaf and choose
    which services are going to run.

    :param torconfig: an instance of txtorcon.TorConfig representing the
                      configuration file.
    """
    root = static.File(STATIC_DIR)

    for path, handler in API.items():
        root.putChild(path, handler())
    reactor.listenTCP(config.panel_port, server.Site(root))

    ## create the hidden service of the panel ##
    if not os.path.exists(PANEL_DIR):
        os.mkdir(PANEL_DIR)
    panel_hs = txtorcon.HiddenService(torconfig, config.tor_data,
            ['%d 127.0.0.1:%d' % (config.panel_port, config.panel_hs_port)])
    hiddenservices['panel'] = panel_hs



if __name__ == '__main__':
    log.startLogging(sys.stdout)
    start_panel()
    reactor.run()

