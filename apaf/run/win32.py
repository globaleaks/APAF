"""
The main file of the apaf on Windows.
"""

from twisted.internet import win32eventreactor
win32eventreactor.install()

from apaf.run import base

setup_complete = base.setup_complete    # XXX: notfy the ui.

def main():
    SysTrayIcon("Anonymous Web Application Framework", default_menu_index=1)
    base.main().addCallback(setup_complete).addErrback(base.setup_failed)

