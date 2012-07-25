"""
APAF Service example: a simple static file web server.
"""
from os.path import join

from twisted.web import static, server
from twisted.python import log

from apaf.core import Service
from apaf import config

class ServiceDescriptor(Service):
    """
    Set up a simple static file server.
    """
    name = 'staticwebserver'
    desc = 'A simple static file server.'
    port = 80

    config = config.Config(
        config_file=join(config.conf_dir, 'static.cfg'),
        defaults={'dirname':'/tmp'},
    )

    def get_factory(self):
        self.resource = static.File(self.config['dirname'])
        return server.Site(self.resource)


