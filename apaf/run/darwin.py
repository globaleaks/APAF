#!/usr/bin/env python
"""
The main file of the apaf.
If assolves three tasks: start a tor instance, start the panel, start services.
"""
from twisted.internet import _threadedselect
_threadedselect.install()

from twisted.internet import reactor
from PyObjCTools import AppHelper
from AppKit import NSNotificationCenter, NSApplication
from apaf.ui import darwin
from AppKit import NSNotificationCenter

from apaf.run import base


def setup_complete(proto):
    NSNotificationCenter.defaultCenter().postNotificationName_object_(
            darwin.TorFinishedLoadNotification, None)
    darwin.embeed_browser()
    base.setup_complete(proto)


def setup_failed(arg):
    base.setup_failed(arg)
    reactor.stop()

def main():
    """
    Setup and start Cocoa GUI main loop
    """
    app = NSApplication.sharedApplication()
    delegate = darwin.ApafAppWrapper.alloc().init()
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
