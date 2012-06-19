#!/usr/bin/env python
"""
The main file of the apaf.
If assolves three tasks: start a tor instance, start the panel, start services.
"""

from apaf import config

if __name__ == '__main__':
    if config.platform == 'win32':
        from run_win32 import main
    elif config.platform == 'darwin':
        from run_darwin import main
    main()
