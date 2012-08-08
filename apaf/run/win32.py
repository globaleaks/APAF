"""
The main file of the apaf on Windows.
"""

from twisted.internet import _threadedselect
_threadedselect.install()

from twisted.internet import reactor
import win32event


from apaf.run import base
from apaf.ui.win32 import SysTrayIcon

setup_complete = base.setup_complete    # XXX: notfy the ui.

def main():
    SysTrayIcon(reactor, start_apaf)

def start_apaf():
    base.main().addCallback(setup_complete).addErrback(base.setup_failed)
    reactor.interleave(win32gui.PumpMessages)
