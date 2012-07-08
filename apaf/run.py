#!/usr/bin/env python
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

def start_tor(torconfig):
    d = txtorcon.launch_tor(torconfig, reactor,
                            progress_updates=updates,
                            tor_binary=tor_binary)
    d.addCallback(setup_complete)
    d.addErrback(setup_failed)

def open_panel_browser():
    """
    Open the default web browser with the panel service.
    """
    import webbrowser
    # xxx . should open localhost, not the .onion
    webbrowser.open(apaf.hiddenservices[0].hs.hostname)

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

    torconfig.HiddenServices = [x.hs for x in apaf.hiddenservices]
    torconfig.save()

    start_tor(torconfig)

    ##  Start the reactor. ##
    #if config.platform == 'darwin':
    #    reactor.interleave(AppHelper.callAfter)
    #else:
    open_panel_browser()
    reactor.run()

def main_win32():
    """
    Custom main for windows.
    """
    # if the compressed zip file does not exists, create it in the current
    # directory of the user.
    if not os.path.exists(config.data_dir):
        from apaf import win32blob  # import the python autoextracter

    main()

def main_darwin():
    """
    Custom main for OSX.
    """
    from PyObjCTools import AppHelper
    from AppKit import NSNotificationCenter, NSApplication
    from apaf.utils.osx_support import ApafAppWrapper, TorFinishedLoadNotification
    from twisted.internet import _threadedselect
    try:
        _threadedselect.install()
    except Exception as e:
        log.err(e)

    app = NSApplication.sharedApplication()
    delegate = ApafAppWrapper.alloc().init()
    delegate.setMainFunction_andReactor_(main, reactor)
    app.setDelegate_(delegate)

    AppHelper.runEventLoop()


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(prog=config.appname, description=config.description)
    parser.add_argument('--debug', action='store_true',  help='Run in debug mode.')
    options = parser.parse_args()

    if options.debug:
        main()
    else:
        strmain = 'main_'+config.platform
        vars().get(strmain, main)()

