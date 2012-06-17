from distutils.core import Command
import subprocess
import objc
import re
import os

from Foundation import *
from AppKit import *
from AppKit import NSNotificationCenter
from PyObjCTools import AppHelper

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
        process = subprocess.Popen("python-config --includes | awk -F'-I' '{print $2}' | sed 's/\/include.*$//'", shell=True, stdout=subprocess.PIPE)
        pythonFrameworkPath = process.stdout.read().strip()
        version = pythonFrameworkPath.split("/")[-1]

        # folder of the app bundle
        frameFolder = "dist/%s.app/Contents/Frameworks/Python.framework/Versions/%s" % (APP_NAME, version)

        # copy it if it does't exists
        if not os.path.exists(frameFolder):
            os.makedirs(frameFolder)
            os.system("cp %s/Python %s" % (pythonFrameworkPath, frameFolder))
            os.system("chmod +x dist/%s.app/Contents/Resources/contrib/tor" % APP_NAME)


class ApafAppWrapper(NSObject):
    """
    Wrapper around the standard apaf runner;
    creates a new icon around the notification centre and controls the apaf.
    """

    statusbar = None
    runApaf = None
    reactor = None
    menuitem = None

    def setMainFunction_andReactor_(self, func, reactor):
        NSLog("set app")
        self.runApaf = func
        self.reactor = reactor

    def applicationDidFinishLaunching_(self, notification):
        statusbar = NSStatusBar.systemStatusBar()
        # Create the statusbar item
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        # set title
        self.statusitem.setTitle_("apaf")
        # Let it highlight upon clicking
        self.statusitem.setHighlightMode_(1)
        # Set tooltip
        self.statusitem.setToolTip_('Anonymous Python Application Framework')
        # set status image
        path = NSBundle.mainBundle().pathForResource_ofType_("status_bar_icon", "png")
        image = NSImage.alloc().initWithContentsOfFile_(path)
        self.statusitem.setImage_(image)

        # Build menu
        self.menu = NSMenu.alloc().init()
        self.menu.setAutoenablesItems_(0)

        self.menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Loading...', 'openAdmin:', '')
        self.menu.addItem_(self.menuitem)

        self.menuitem.setEnabled_(0)
        print "is it %d" % self.menuitem.isEnabled()
        # Default event
        quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menu.addItem_(quit)
        # Bind it to the status item
        self.statusitem.setMenu_(self.menu)

        # listen for completed notification
        sel = objc.selector(self.torHasLoaded, signature='v@:')

        ns = NSNotificationCenter.defaultCenter()
        ns.addObserver_selector_name_object_(self, sel, TorFinishedLoadNotification, None)

        self.runApaf()

    def torHasLoaded(self):
        self.menuitem.setTitle_("Open service in browser")
        self.menuitem.setEnabled_(1)
        pass

    def applicationShouldTerminate_(self, sender):
        if self.reactor.running:
            self.reactor.addSystemEventTrigger(
                'after', 'shutdown', AppHelper.stopEventLoop)
            self.reactor.stop()
            return False
        return True

    def openAdmin_(self, sender):
        url = NSURL.URLWithString_(NSString.stringWithUTF8String_("http://localhost:4242"))
        NSWorkspace.sharedWorkspace().openURL_(url)

