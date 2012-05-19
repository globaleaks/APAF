"""
Configuration handler for the APAF.
"""
from __future__ import with_statement

import sys
import yaml
import os
import os.path


class Config(object):
    """
    Configuration class
    """
    _root_dir = os.path.abspath(__file__).rsplit('APAF', 1)[0] + 'APAF'
    _conf_dir = (os.path.expanduser('~/.apaf/')  if sys.platform != 'win32'
                 else os.path.expanduser('~/Apaf'))

    platform = sys.platform
    config_file = os.path.join(_conf_dir, 'apaf.cfg')
    log_file = os.path.join(_conf_dir, 'apaf.log')
    binary_kits = os.path.join(_root_dir, 'contrib')
    tor_data = os.path.join(_conf_dir, 'tordata')
    panel_port = 4242
    panel_hs_port = 80

    def __init__(self):
        if not os.path.exists(os.path.dirname(self.config_file)):
            os.mkdir(os.path.dirname(self.config_file))
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as cfg:
                # XXX. add keys with their default values.
                cfg.write('dio: cane\n')

        with open(self.config_file, 'r') as cfg:
            for key, value in (yaml.load(cfg) or dict()).iteritems():
                setattr(self, key, value)

    def __setattr__(self, name, value):
        """
        Mask the standard setattr method to deny dunder variables assignment.
        """
        if name.startswith('_') and not name[0].isdigit():
            raise ValueError('Configuration variables must start with an ascii'
                              'lowercase letter.')
        else:
            self.__dict__[name] = value

    def __delattr__(self, name):
        raise ValueError("Refusing to remove " + name)

    def repl(self):
        return str(vars(self))

    def commit(self):
        yaml.dump(vars(self), stream=self.config_file)


config = Config()
