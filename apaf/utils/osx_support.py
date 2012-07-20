from distutils.core import Command
import subprocess
import os

import objc
import AppKit
import WebKit
import Foundation
from PyObjCTools import AppHelper
from twisted.python import log

import apaf
from apaf import config

TorFinishedLoadNotification = 'TorFinishedLoadNotification'

class OSXPatchCommand(Command):
    """
    OSX specific patch command. ## XXX. needed or not just for lion?
    """
    description = "Patch for OS X 10.7 (lion) bug -> Python.framework not copied inside app bundle"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        if not os.path.exists("dist/%s.app/" % config.appname):
            log.error("You have to run py2app first")
            return
        # getting Python.framework path
        cmd = "python-config --includes | awk -F'-I' '{print $2}' | sed 's/\/include.*$//'"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        pythonFrameworkPath = process.stdout.read().strip()
        version = pythonFrameworkPath.split("/")[-1]

        # folder of the app bundle
        frameFolder = ("dist/%s.app/Contents/Frameworks/Python.framework/Versions/%s"
                       % (config.appname, version))

        # copy it if it does't exists
        if not os.path.exists(frameFolder):
            os.makedirs(frameFolder)
            os.system("cp %s/Python %s" % (pythonFrameworkPath, frameFolder))
            os.system("chmod +x dist/%s.app/Contents/Resources/contrib/tor" % config.appname)


<<<<<<< HEAD
class ApafAppWrapper(Foundation.NSObject):
=======
class ApafAppWrapper(AppKit.NSObject):
>>>>>>> 46a3a3c5828e3a27f19a74ba8ca035792b304bce
    """
    Wrapper around the standard apaf runner;
    creates a new icon around the notification centre and controls the apaf.
    """

    statusbar = None
    runApaf = None
    reactor = None
    menuitem = None

    def setMainFunction_andReactor_(self, func, reactor):
<<<<<<< HEAD
        log.msg('setting up application')
=======
        AppKit.NSLog("set app")
>>>>>>> 46a3a3c5828e3a27f19a74ba8ca035792b304bce
        self.runApaf = func
        self.reactor = reactor

    def applicationDidFinishLaunching_(self, notification):
        statusbar = AppKit.NSStatusBar.systemStatusBar()
        # Create the statusbar item
        self.statusitem = statusbar.statusItemWithLength_(AppKit.NSVariableStatusItemLength)
        # set title
        self.statusitem.setTitle_(config.appname)
        # Let it highlight upon clicking
        self.statusitem.setHighlightMode_(1)
        # Set tooltip
        self.statusitem.setToolTip_(config.description)
        # set status image
        path = AppKit.NSBundle.mainBundle().pathForResource_ofType_("status_bar_icon", "png")
        image = AppKit.NSImage.alloc().initWithContentsOfFile_(path)
        self.statusitem.setImage_(image)

        # Build menu
        self.menu = AppKit.NSMenu.alloc().init()
        self.menu.setAutoenablesItems_(0)

        self.menuitem = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                'Loading...', 'openAdmin:', '')
        self.menu.addItem_(self.menuitem)

        self.menuitem.setEnabled_(0)
        # Default event
        quit = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menu.addItem_(quit)
        # Bind it to the status item
        self.statusitem.setMenu_(self.menu)

        # listen for completed notification
        sel = objc.selector(self.torHasLoaded, signature='v@:')

        ns = AppKit.NSNotificationCenter.defaultCenter()
        ns.addObserver_selector_name_object_(self, sel, TorFinishedLoadNotification, None)

        self.runApaf()

    def torHasLoaded(self):
        self.menuitem.setTitle_("Open service in browser")
        self.menuitem.setEnabled_(1)

    def applicationShouldTerminate_(self, sender):
        if self.reactor.running:
            self.reactor.addSystemEventTrigger(
                'after', 'shutdown', AppHelper.stopEventLoop)
            self.reactor.stop()
            return False
        return True

    def openAdmin_(self, sender):
        """
        Check if apaf's window is already open, otherwise launch it.
        XXX. should display also a dock icon.
        """
        embeed_browser()


def embeed_browser(host=None):
    """
    Open a new window displaying a web page using WebKit.
    :param host: hostname to view. if not set, uses panel configuration page.

    """
    app = AppKit.NSApplication.sharedApplication()
    rect = Foundation.NSMakeRect(600,400,600,800)
    win = AppKit.NSWindow.alloc()
    win.initWithContentRect_styleMask_backing_defer_(
            rect,
            AppKit.NSTitledWindowMask |
            AppKit.NSClosableWindowMask |
            AppKit.NSResizableWindowMask |
            AppKit.NSMiniaturizableWindowMask,
            AppKit.NSBackingStoreBuffered,
            False)
    win.display()
    win.orderFrontRegardless()

    webview = WebKit.WebView.alloc()
    webview.initWithFrame_(rect)

    if not host:
        host = apaf.hiddenservices[0].tcp.getHost()
        host = (host.host if not host.host.startswith('0.0') else '127.0.0.1',
                host.port)
<<<<<<< HEAD

    url = Foundation.NSURL.URLWithString_(Foundation.NSString.stringWithUTF8String_(
        "http://%s:%s" % host))
=======
    print "http://%s:%s" % (host[0], host[1])
    url = AppKit.NSURL.URLWithString_(AppKit.NSString.stringWithUTF8String_(
        "http://%s:%s" % (host[0], host[1])))

>>>>>>> 46a3a3c5828e3a27f19a74ba8ca035792b304bce
    req = Foundation.NSURLRequest.requestWithURL_(url)
    webview.mainFrame().loadRequest_(req)

    win.setContentView_(webview)
    app.run()
