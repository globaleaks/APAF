from twisted.internet import gtk2reactor # for gtk-2.0
gtk2reactor.install()

from twisted.internet import reactor
from apaf.ui.gtk import GTKGui


def main():
    base.main()
    GTKGui()
