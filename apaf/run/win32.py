"""
The main file of the apaf on Windows.
"""

from twisted.internet import win32eventreactor
win32eventreactor.install()

from twisted.internet import reactor
from apaf.run import base
from apaf.utils.win32_support import SysTrayIcon

setup_complete = base.setup_complete    # XXX: notfy the ui.

def main():
    base.main().addCallback(setup_complete).addErrback(base.setup_failed)
    reactor.run()
    SysTrayIcon("Anonymous Web Application Framework", default_menu_index=1)

