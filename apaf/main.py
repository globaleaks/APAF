#!/usr/bin/env python
"""
Maain file.
After detecting the platform on which it is running, launches its relative
main() from the apaf.run package.
"""
from argparse import ArgumentParser
from apaf import config


def std_main():
    from apaf.run import base
    from twisted.internet import reactor

    base.main().addCallback(base.setup_complete).addErrback(base.setup_failed)
    reactor.run()


parser = ArgumentParser(prog=config.appname, description=config.description)
parser.add_argument('--debug', action='store_true',  help='Run in debug mode.')
options = parser.parse_args()

if options.debug:
    main = std_main
else:
    try:
        main = __import__('apaf.run.'+config.platform, fromlist=['main']).main
    except ImportError:
        main = std_main

main()

