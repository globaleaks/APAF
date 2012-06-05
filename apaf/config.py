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
    _data_dir = os.path.join(_root_dir, 'datadir')
    _conf_dir = os.path.join(_data_dir, 'config')

    platform = sys.platform
    config_file = os.path.join(_conf_dir, 'apaf.cfg')
    log_file = os.path.join(_conf_dir, 'apaf.log')
    binary_kits = os.path.join(_data_dir, 'contrib')
    tor_data = os.path.join(_conf_dir, 'tordata')
    services_dir = os.path.join(_data_dir, 'services')
    static_dir = os.path.join(services_dir, 'panel', 'static')
    base_port = 4242
    services = dict()    # list of services to be started.

    def __init__(self):
        """
        Load the configuration from the cfg file.
        If apaf's configuration and status directories are not ready, create
        them.
        """
        # check for directory path
        if not os.path.exists(self._conf_dir):
            os.mkdir(self._conf_dir)
        if not os.path.exists(self.tor_data):
            os.mkdir(self.tor_data)

        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as cfg:
                # XXX. add keys with their default values.
                cfg.write('dio: cane\n')

        # load configuration
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
        raise AttributeError("Refusing to remove " + name)

    def __repl__(self):
        return str(vars(self))

    def commit(self):
        with open(self.config_file, 'w') as cfg:
            yaml.dump(vars(self), stream=cfg)


config = Config()
