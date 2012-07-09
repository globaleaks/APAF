#!/usr/bin/env python
from argparse import ArgumentParser
from apaf import config

parser = ArgumentParser(prog=config.appname, description=config.description)
parser.add_argument('--debug', action='store_true',  help='Run in debug mode.')
options = parser.parse_args()

def std_main():
    from apaf.run import base
    from twisted.internet import reactor

    base.main()
    base.open_panel_browser()
    reactor.run()


if options.debug:
    main = std_main
else:
    try:
        main = __import__('apaf.run.'+config.platform, fromlist=['main']).main
    except ImportError:
        main = std_main

main()

