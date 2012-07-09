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
from apaf import core, config
from apaf.panel import panel
from apaf.run import base


def setup_complete(proto):
    NSNotificationCenter.defaultCenter().postNotificationName_object_(
            TorFinishedLoadNotification, None)

    base.setup_complete(proto)


def setup_failed(arg):
    base.setup_failed(arg)
    reactor.stop()

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
    base.main().addCallback(setup_complete).addErrback(setup_failed)
    reactor.interleave(AppHelper.callAfter)


if __name__ == '__main__':
    main()
