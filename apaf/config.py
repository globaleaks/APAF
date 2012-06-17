"""
Configuration handler for the APAF.
"""
from __future__ import with_statement

import sys
import yaml
import os
import os.path


def _get_datadir():
    """
    Looks up for the data directory checking whether the application path
    is avaible. Path checking order:
     (i)   /etc,
     (ii)  ~/.config,
     (iii) environment variables,
     (iv)  package path,
     (v)   current directory.
    For more informations, see  issue #16.
    """
    homedir = os.path.expanduser(os.path.join('~', '.apaf', 'datadir'))
    if os.path.exists(homedir):
        return homedir

    sysdir = '/usr/share/apaf/datadir'
    if os.path.exists(sysdir):
        return sysdir

    bundledir = os.environ.get('RESOURCEPATH')
    if bundledir:
        return bundledir

    vanilladir = os.path.join(package_dir, '..', 'datadir')
    if os.path.exists(vanilladir):
        return vanilladir

    curdir = os.path.join('datadir', )
    if os.path.exists(curdir):
        return curdir
    else:
        # import blobbone
        return curdir


appname = 'apaf'
package_dir = os.path.abspath(os.path.dirname(__file__))
platform = sys.platform
data_dir = _get_datadir()
conf_dir = os.path.join(data_dir, 'config')
config_file = os.path.join(conf_dir, 'apaf.cfg')
log_file = os.path.join(conf_dir, 'apaf.log')
binary_kits = os.path.join(data_dir, 'contrib')
tor_data = os.path.join(conf_dir, 'tordata')
services_dir = os.path.join(data_dir, 'services')
static_dir = os.path.join(services_dir, 'panel', 'static')


class Config(object):
    """
    Configuration class
    """
    base_port = 4242
    services = dict()    # list of services to be started.

    def __init__(self):
        """
        Load the configuration from the cfg file.
        If apaf's configuration and status directories are not ready, create
        them.
        """
        # check for directory path
        if not os.path.exists(conf_dir):
            os.mkdir(conf_dir)
        if not os.path.exists(tor_data):
            os.mkdir(tor_data)

        if not os.path.exists(config_file):
            with open(config_file, 'w') as cfg:
                # XXX. add keys with their default values.
                cfg.write('dio: cane\n')

        # load configuration
        with open(config_file, 'r') as cfg:
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
        with open(config_file, 'w') as cfg:
            yaml.dump(vars(self), stream=cfg)


custom = Config()
