#!/usr/bin/env python
"""
Maain file.
After detecting the platform on which it is running, launches its relative
main() from the apaf.run package.
"""
from optparse import OptionParser

import sys
import os
import os.path
try:
    from apaf import config
except ImportError:
    import sys
    import os.path
    import os
    if 'RESOURCEPATH' in os.environ:
        # if we are running on osx put our bundled libraries first in system's
        # path.
        sys.path.insert(0, os.path.join(os.environ['RESOURCEPATH'], 'lib', 'python2.7', 'lib-dynload'))
    import config
    import os.path
    sys.path.insert(0, os.path.join(config.package_dir, '..'))


def std_main():
    from apaf.run import base
    from twisted.internet import reactor

    base.main().addCallback(base.setup_complete).addErrback(base.setup_failed)
    reactor.run()


parser = OptionParser(prog=config.appname,
                      description=config.description)
parser.add_option('--debug', action='store_true',  help='Run in debug mode.')
options, args = parser.parse_args()

if options.debug:
    main = std_main
else:
    try:
        main = __import__('apaf.run.'+config.platform, fromlist=['main']).main
    except ImportError:
        main = std_main

main()

