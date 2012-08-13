#-*- coding: UTF-8 -*-
import urlparse

from txtorcon import torcontrolprotocol
from twisted.internet import defer
from twisted.python import failure
from cyclone.escape import json_encode, json_decode
from cyclone import web

import apaf
from apaf import config
from apaf.panel import controllers

from base import PanelHandler

def render(page, _authenticated=False, **args):
    """
    Simple helper function for returning a PanelHandler page.
    :param page: path for html page
    :param _handler_name: classname for the handler (useful in debugging)
    :param args: arguments for html
    """
    def get(self):
        self.render(page, **args)

    return type('Handler_'+page, (PanelHandler,),
                {'get': get if not _authenticated else web.authenticated(get)})

def render_with_controller(page, controller, *args, **kwargs):
    """
    Simple factory function for rendering html pages.
    :param page: path for html page.
    :param _handler_name: classname for the handler (useful in debugging)
    :param *args, **kwargs: arguments to the controller.
    :ret: a PanelHandler object.
    """
    controller = controller()
    def get(self):
        return self.render(page, **controller.get(*args, **kwargs))

    return type('Handler_'+page, (PanelHandler, ),
                {'get': get})



class ConfigHandler(PanelHandler):
    controller = controllers.ConfigCtl()

    def parse_type(self, var):
        if var in (True, False, None):
            return 'checkbox'
        elif hasattr(var, 'open') and hasattr(var, 'close'):
            return 'file'
        else:
            return 'text'

    @web.authenticated
    def get(self):
        return self.render(
               'config.html',
               entries=dict((key, {'value':value, 'type':self.parse_type(value)}) for
                             key, value in self.controller.get().iteritems())
        )

class ServiceHandler(PanelHandler):
    controller = controllers.ServicesCtl()

    @web.authenticated
    def get(self):
        service = self.get_argument('service', None)
        return self.render('services.html' if not service else 'serviceinfo.html',
                           services=self.controller.get(service))


class LoginHandler(PanelHandler):
    REDIRECT = '/'

    def get(self):
        if not self.get_current_user():
            return self.render('login.html')
        else: self.redirect(self.REDIRECT)

    def post(self):
        request, = urlparse.parse_qs(self.requestbody).get('passwd', ['', ])

        if not self.auth_login(request['passwd']):
            raise web.HTTPAuthenticationRequired
        else:
            return self.redirect(self.REDIRECT)


class TorHandler(PanelHandler):
    controller = controllers.TorCtl()

    @web.authenticated
    @defer.inlineCallbacks
    def get(self):
        bootstrap = yield self.controller.get('status/bootstrap-phase')
        self.render('tor.html',
                    version=apaf.torctl.version,
                    bootstrap=bootstrap,
        )
