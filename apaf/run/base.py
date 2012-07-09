
"""
The main file of the apaf.
If assolves three tasks: start a tor instance, start the panel, start services.
"""
import functools
import os
import os.path
import sys
import tempfile

from twisted.internet import reactor, protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.python import log
import txtorcon

import apaf
from apaf import core
from apaf import config
from apaf.panel import panel

tor_binary = (os.path.join(config.binary_kits, 'tor') +
              ('.exe' if config.platform == 'win32' else ''))

def setup_complete(proto):
    """
    Callback: fired once tor has been started.
    """
    apaf.torctl = proto.tor_protocol
    for service in apaf.hiddenservices:
        log.msg('%s service running at %s' % (service, service.hs.hostname))


def updates(prog, tag, summary):
    log.msg("%d%%: %s" % (prog, summary))

def setup_failed(arg):
    """
    Callback: fired whether launching tor has failed.
    """
    log.err('Setup failed. -%s-' %  arg)
    reactor.stop()

def open_panel_browser():
    """
    Open the default web browser with the panel service.
    """
    import webbrowser
    # xxx . should open localhost, not the .onion
    webbrowser.open(apaf.hiddenservices[0].hs.hostname)

def main(progress_updates=updates):
    """
    Start logging, apaf services, and tor.

    :param progress_updates: a callback fired during tor's bootstrap.
    :ret: a twisted Deferred object for setting up callbacks in case of
          sucess/errors.
    """
    ## start the logger. ##
    log.startLogging(sys.stdout)
    torconfig = txtorcon.TorConfig()

    ## start apaf. ##
    panel.start_panel(torconfig)
    core.start_services(torconfig)

    torconfig.HiddenServices = [x.hs for x in apaf.hiddenservices]
    torconfig.save()

    ## start tor. ##
    return txtorcon.launch_tor(torconfig, reactor,
                               progress_updates=progress_updates,
                               tor_binary=tor_binary)
