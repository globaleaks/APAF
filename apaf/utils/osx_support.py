from distutils.core import Command
import subprocess
import objc
import re
import os
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper

APP_NAME = 'apaf' # @TODO must me in some other place in a config from which setup() also can read it (must m ethe same :P)

#
# OS X specific patch command it is needed under OS X 10.7 (lion)
#
class OSXPatchCommand(Command):
    description = "Patch for OS X 10.7 (lion) bug -> Python.framework not copied inside app bundle"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        if not os.path.exists("dist/%s.app/" % APP_NAME):
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

    # -- class OSXPatchCommand

import objc, re, os
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper


class ApafAppWrapper(NSObject):
    statusbar = None
    runApaf = None
    reactor = None

    def setMainFunction_andReactor_(self, func, reactor):
        NSLog("set app")
        self.runApaf = func
        self.reactor = reactor

    def applicationDidFinishLaunching_(self, notification):
        statusbar = NSStatusBar.systemStatusBar()
        # Create the statusbar item
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        
        self.statusitem.setTitle_("apaf")
        # Let it highlight upon clicking
        self.statusitem.setHighlightMode_(1)
        # Set a tooltip
        self.statusitem.setToolTip_('Anonymous Python Application Framework')
        path = NSBundle.mainBundle().pathForResource_ofType_("status_bar_icon", "png")
        print path
        image = NSImage.alloc().initWithContentsOfFile_(path)
        self.statusitem.setImage_(image)
        #status_item.setImage_(image)

        # Build a very simple menu
        self.menu = NSMenu.alloc().init()
        # Sync event is bound to sync_ method
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Open admin interface', 'openAdmin:', '')

        self.menu.addItem_(menuitem)
        # Default event
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menu.addItem_(menuitem)
        # Bind it to the status item
        self.statusitem.setMenu_(self.menu)
        #sel = objc.selector(self.setApafStart,signature='v@:')
        #self.performSelectorInBackground_withObject_(sel, None)
        self.runApaf()
        
    
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

