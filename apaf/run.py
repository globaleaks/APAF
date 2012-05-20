"""
The main file of the apaf.
If assolves three tasks: start a tor instance, start the panel, start services.
"""

import functools
import os
import os.path
import sys
import tempfile

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.web import server, resource
from twisted.python import log
import txtorcon

import apaf
from apaf import core
from apaf.panel import panel
from apaf.config import config


tor_binary = (os.path.join(config.binary_kits, 'tor') +
              ('.exe' if config.platform == 'win32' else ''))

def setup_complete(proto):
    for name, hs in apaf.hiddenservices.iteritems():
        log.msg('%s service running at %s' % (name, hs.hostname))


def updates(prog, tag, summary):
    log.msg("%d%%: %s" % (prog, summary))

def setup_failed(arg):
    log.err('Setup failed. -%s-' %  arg)
    reactor.stop()

def start_tor(torconfig):
    d = txtorcon.launch_tor(torconfig, reactor,
                            progress_updates=updates,
                            tor_binary=tor_binary)
    #d.addCallback(setup_complete)
    d.addErrback(setup_failed)

def main():
    """
    Start the apaf.
    """
    ## start the logger. ##
    log.startLogging(sys.stdout)
    torconfig = txtorcon.TorConfig()

    ## start apaf. ##
    panel.start_panel(torconfig)
    core.start_services(torconfig)

    torconfig.HiddenServices = apaf.hiddenservices.values()
    torconfig.save()

    start_tor(torconfig)

    ##  Start the reactor. ##
    reactor.run()


if __name__ == '__main__':
    main()
    import webbrowser
#    webbrowser.open(apaf.hiddenservices['panel'].hostname)
