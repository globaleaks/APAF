"""
Configuration manager for APAF.
Holds global state variables and custom configurations.
"""
from __future__ import with_statement

import sys
import yaml
import os
import os.path
from copy import deepcopy
from hashlib import sha256

from Crypto.Random import get_random_bytes

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

#     try:
#         import pkg_resources as pkg
#         # eggdir =   ## XXX: the .egg directory.
#     except ImportError:
#         log.err('Unable to import setuptools')
#
    curdir = os.path.join(os.getcwd(), 'datadir', )
    if os.path.exists(curdir):
        return curdir
    else:
        import apaf.blobbone
        return curdir


def _get_torbinary():
    """
    Attempts to retrieve tor executable, looking in the following order:
    (i) binary kits : datadir/contrib/tor
    (ii) emulate `which` command and looks inside $PATH
    """
    bundle = os.path.join(binary_kits, 'tor')
    if platform == 'win32': bundle += '.exe'
    if os.path.exists(bundle): return bundle

    for installdir in os.environ['PATH'].split(':'):
        if 'tor' in os.listdir(installdir):
            return os.path.join(installdir, 'tor')


appname = 'apaf'
description = 'An Anonymous Web Application Framework'
package_dir = os.path.abspath(os.path.dirname(__file__))
platform = sys.platform
data_dir = _get_datadir()
conf_dir = os.path.join(data_dir, 'config')
config_file = os.path.join(conf_dir, 'apaf.cfg')
log_file = os.path.join(conf_dir, 'apaf.log')
binary_kits = os.path.join(data_dir, 'contrib')
tor_binary = _get_torbinary()
tor_data = os.path.join(conf_dir, 'tordata')
services_dir = os.path.join(data_dir, 'services')
static_dir = os.path.join(services_dir, 'panel', 'static')
drawable_dir = os.path.join(data_dir, 'drawable')

# check for directory path
if not os.path.exists(conf_dir):
    os.mkdir(conf_dir)
if not os.path.exists(tor_data):
    os.mkdir(tor_data)

class Config(object):
    """
    Configuration class
    """
    __slots__ = ('defaults', 'config_file', 'vars')

    def __init__(self, defaults, config_file):
        """
        Load the configuration from the cfg file.
        If apaf's configuration and status directories are not ready, create
        them.
        """
        self.defaults = defaults
        self.config_file = config_file

        if not os.path.exists(self.config_file):
            self.reset()
        else:    # load configuration
            self.vars = dict()
            with open(self.config_file, 'r') as cfg:
                for key, value in (yaml.safe_load(cfg) or dict()).iteritems():
                    self[key] = value

    def __getitem__(self, name):
        return self.vars[name]

    def __setitem__(self, name, value):
        """
        Mask the standard setattr method to deny new configurations or
        writing different types.
        """
        if name not in self.defaults:
            raise KeyError(name)
        if value.__class__ != self.defaults[name].__class__:
            raise TypeError('%s:%s is not of type %s' % (name, value, type(value)))
        self.vars[name] = value

    def __delitem__(self, name):
        raise AttributeError("Refusing to remove " + name)

    def __contains__(self, elt):
        return elt in self.vars

    def __iter__(self):
        return self.vars.iteritems()

    def __repl__(self):
        return '<Config object %s>' % self.vars

    def commit(self):
        with open(self.config_file, 'w') as cfg:
            yaml.safe_dump(self.vars, stream=cfg)
        return True

    def reset(self):
        """
        Restores default configuration.
        """
        self.vars = deepcopy(self.defaults)
        self.commit()


custom = Config(config_file=config_file,
                defaults=dict(
                    base_port=4242,
                    services=['staticwebserver'],    # list of services to be started
                    passwd=sha256('None').hexdigest(),
                    cookie_secret=get_random_bytes(100),
                ))
