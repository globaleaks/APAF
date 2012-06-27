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

from twisted.internet import _threadedselect
_threadedselect.install()

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.web import server, resource
from twisted.python import log
import txtorcon


from PyObjCTools import AppHelper
from AppKit import NSNotificationCenter, NSApplication
from apaf.utils.osx_support import ApafAppWrapper, TorFinishedLoadNotification
from AppKit import NSNotificationCenter

import apaf
from apaf import core
from apaf import config
from apaf.panel import panel

tor_binary = os.path.join(config.binary_kits, 'tor')

def setup_complete(proto):
    NSNotificationCenter.defaultCenter().postNotificationName_object_(TorFinishedLoadNotification, None)

    for service in apaf.hiddenservices:
        log.msg('%s service running at %s' % (service, service.hs.hostname))


def updates(prog, tag, summary):
    log.msg("%d%%: %s" % (prog, summary))

def setup_failed(arg):
    log.err('Setup failed. -%s-' %  arg)
    reactor.stop()

def start_tor(torconfig):
    d = txtorcon.launch_tor(torconfig, reactor,
                            progress_updates=updates,
                            tor_binary=tor_binary)
    d.addCallback(setup_complete)
    d.addErrback(setup_failed)

def main():
    """
    Setup and start Cocoa GUI main loop
    """
    app = NSApplication.sharedApplication()
    delegate = ApafAppWrapper.alloc().init()
    delegate.setMainFunction_andReactor_(start_apaf, reactor)
    app.setDelegate_(delegate)

    AppHelper.runEventLoop()


def start_apaf():
    """
    Start the apaf.
    It gets called asyncronously by ApafAppWrapper didFinishLoading
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

    reactor.interleave(AppHelper.callAfter)


if __name__ == '__main__':
    main()
