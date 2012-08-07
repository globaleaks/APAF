"""
The basic apaf panel, accessible as it is from
"""
import os
import os.path
import sys

from twisted.internet import reactor
from twisted.python import log
from cyclone import web
import txtorcon

import apaf
from apaf.core import Service, add_service
from apaf import config
from apaf.panel import handlers, controllers



class PanelService(Service):
    name = 'panel'
    desc = 'Administration panel and apaf manager.'
    port = 80
    icon = None

    static_dir = os.path.join(config.services_dir, 'panel', 'static')
    templates_dir = os.path.join(config.services_dir, 'panel', 'templates')

    _paneldir = os.path.join(config.services_dir, 'panel')
    urls = [
        ## REST API ##
        # services informations
        (r'/services/(.*)/start', handlers.ServiceHandler, {'action':'start'}),
        (r'/services/(.*)/stop', handlers.ServiceHandler, {'action':'stop'}),
        (r'/services/(.*)', handlers.ServiceHandler, {'action':'state'}),
        (r'/services', handlers.ServiceHandler),
        # authentication
        (r'/auth/login', handlers.AuthHandler, {'action':'login'}),
        (r'/auth/logout', handlers.AuthHandler, {'action':'logout'}),
        # configuration
        (r'/config', handlers.ConfigHandler),
        # tor controlport
        (r'/tor', handlers.TorHandler),
        (r'/tor/(.*)', handlers.TorHandler),

        (r'/', handlers.IndexHandler),

        # Legacy html
        (r'/index.html', handlers.render('index.html')),
        (r'/services.html', handlers.ServicesHtmlHandler),
        (r'/tor.html', handlers.render('tor.html')),
        (r'/config.html', handlers.ConfigHtmlHandler),
        (r'/about.html', handlers.render('about.html')),
        (r'/login.html', handlers.render('login.html')),

        # JS Application
        (r'/app.html', handlers.render('index.html')),

        ## STATIC FILES ##
        (r'/(.*)', web.StaticFileHandler, {'path':static_dir}),
    ]

    def get_factory(self):
        # create the hidden service directory of the panel
        if not os.path.exists(self._paneldir):
            os.mkdir(self._paneldir)

        return web.Application(self.urls,
                               debug=True,
                               cookie_secret=config.custom['cookie_secret'],
                               login_url='/',
                               xsrf_cookies=True,
                               template_path = self.templates_dir,
        )

def start_panel(torconfig):
    """
    Set up the panel service, which lets the user customize apaf and choose
    which services are going to run.

    :param torconfig: an instance of txtorcon.TorConfig representing the
                      configuration file.
    """
    panel = PanelService()
    add_service(torconfig, panel)


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    start_panel(txtorcon.TorConfig())
    reactor.run()
