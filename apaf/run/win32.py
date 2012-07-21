"""
The main file of the apaf on Windows.
"""

from twisted.internet import _threadedselect
_threadedselect.install()

from twisted.internet import reactor
from apaf.run import base
from apaf.utils.win32_support import SysTrayIcon

setup_complete = base.setup_complete    # XXX: notfy the ui.

def main():
    SysTrayIcon(reactor, start_apaf)

def start_apaf():
    base.main().addCallback(setup_complete).addErrback(base.setup_failed)
    reactor.interleave(lambda: None)
