try:
    import pygtk
    pygtk.require('2.0')
    import gtk
except ImportError:
    raise RuntimeError('cannot load GUI Libraries.')

from apaf import config
from apaf.run import base


class GTKGui:
    def __init__(self):
        self.tray = gtk.StatusIcon()
        self.tray.set_from_stock(gtk.STOCK_ABOUT)
        self.tray.connect('popup-menu', self.on_right_click)
        self.tray.set_tooltip(config.description)

        reactor.run()
        gtk.main()


    def on_right_click(self, icon, event_button, event_time):
        self.make_menu(event_button, event_time)

    def make_menu(self, event_button, event_time):
        menu = gtk.Menu()

        panel = gtk.MenuItem('Panel')
        panel.show()
        menu.append(panel)
        panel.connect('activate', self.on_panel)

        about = gtk.MenuItem('About')
        about.show()
        menu.append(about)
        about.connect('activate', self.on_about)

        quit = gtk.MenuItem('Quit')
        quit.show()
        menu.append(quit)
        quit.connect('activate', gtk.main_quit)

        menu.popup(None, None, gtk.status_icon_position_menu,
                   event_button, event_time, self.tray)

    def on_about(self, widget):
        dialog = gtk.AboutDialog()
        dialog.set_destroy_with_parent(True)
        dialog.set_icon_name()
        dialog.set_name(config.appname)
        dialog.set_version(apaf.__version__)
        dialog.set_copyright(apaf.__copyright__)
        dialog.set_comments(config.description)
        dialog.set_authors([apaf.__author__])
        dialog.run()
        dialog.destroy()

    def on_panel(self, widget):
        base.open_panel_browser()

