#-*- coding: UTF-8 -*-

from txtorcon import torcontrolprotocol
from twisted.internet import defer
from twisted.python import failure
from cyclone import web
from cyclone.escape import json_encode, json_decode

import apaf
from apaf import config
from apaf.panel import controllers
from base import PanelHandler

class RestHandler(PanelHandler):
    """
    A simple RequestHandler with utils for the panel
    """

    def initialize(self, action=None):
        self.action = action

    def error(self, msg):
        """
        Performs JSON response:
         * {"error" : error message }

        :param msg: error message
        """
        return json_encode({'error': str(msg)})

    def result(self, boolean):
        """
        Performs JSON response:
         * {"result" : true}
         * {"result": false}
        :param boolean: the boolean to be returned
        """
        return json_encode({'result':boolean})

    def set_default_headers(self):
        """
        Panel API is performed entirely via json calls.
        """
        self.set_header('Content-Type', 'application/json')

    def finish_json(self, infos):
        return self.finish(json_encode(infos))


class AuthHandler(RestHandler):
    """
    Authentication:
        ** shall check if requests come from localhost?
        ** just oauth login?
        ***
    """
    _actions = ['login', 'logout']
    _uid_cookie = 'user'

    def initialize(self, action):
        if action not in self._actions:
            raise ValueError('Unexpected action')
        else:
            self.action = action

    def post(self):
        """
        Processes asyncronous request:
            * GET /auth/login
        """
        if self.action != 'login':
            raise web.HTTPError(404)

        # if self.request.remote_ip == '127.0.0.1':
        #     self.set_secure_cookie(self._uid_cookie, config.custom['passwd'])
        #     return self.write(self.result(True))

        if not self.application.conf['remote_login']:
            raise web.HTTPAuthenticationRequired

        request = json_decode(self.request.body)
        if 'passwd' not in request:
            return self.error('invalid request')
        elif not self.get_current_user(request['passwd']):
            return self.write(self.error('login failed'))
        else:
            self.set_secure_cookie('auth', request['passwd'])
            return self.write(self.result(True))

    @web.authenticated
    def get(self):
        """
        Process asycnronous request:
            * GET /auth/logout
        """
        if self.action != 'logout':
            raise web.HTTPAuthenticationRequired if not self.current_user \
                  else web.HTTPError(404)

        #if not self.user:
        #    raise HTTPError(403)
        self.clear_cookie(self._uid_cookie)


class ConfigHandler(RestHandler):
    """
    Handler for editing config.custom.
    """
    controller = controllers.ConfigCtl()

    @web.authenticated
    def get(self):
        """
        Process GET requests:
            * /config
        Return a dictionary item:value for each item configurable from the
        panel.
        """
        return self.write(json_encode(self.controller.get()))

    @web.authenticated
    def put(self):
        """
        Processes PUT requests:
            * /config
        """
        if not self.request.headers.get('Settings'):
            return self.error('invalid query')
        try:
            self.write(self.result(self.controller.set(
                json_decode(self.request.headers['Settings']))))
        except ValueError as exc:
            return self.write(self.error(exc))

    @web.authenticated
    def post(self):
        """
        Processes POST requests:
            * /config

        <hellais> maker: sure. Though it's recommended to also create
                  the equivalent POST based method since certain browsers/HTTP
                  clients don't support PUT method
        """
        if not self.request.body:
            return self.error('invalid query')
        try:
            self.write(json_decode(self.request.body))
        except ValueError as exc:
            return self.error(exc)


class ServiceHandler(RestHandler):
    _actions = ['state', 'start', 'stop']
    controller = controllers.ServicesCtl()

    def state(self, service):
        """
        Process GET request:
            * /services/<service>/
        Return a dictionary containig a summary of what the service is and on
        which url is running on.
        """
        try:
            return json_encode(self.controller.get(service))
        except ValueError:
            raise web.HTTPError(404)

    def start(self, service):
        """
        Process GET request:
            * /services/<service>/start
        """

    @defer.inlineCallbacks
    def stop(self, service):
        """
        Process GET request:
            * /services/<service>/stop
        """
        try:
            ret = yield self.controller.set(service, False)
        except ValueError:
            raise web.HTTPError(404)

        defer.returnValue(self.result(ret))

    @web.asynchronous
    @web.authenticated
    def get(self, service=None):
        """
        Processes GET requests:
          * /services/
          * /services/<service>/
          * /services/<service>/start
          * /services/<service>/stop
        """
        if self.action not in self._actions:
            raise web.HTTPError(404)

        ret = defer.maybeDeferred(getattr(self, self.action), service)
        ret.addCallback(self.callback_success).addErrback(self.callback_exception)

    def callback_success(self, infos):
        self.finish(infos)

    def callback_exception(self, exc):
        self.send_error(exc.value.status_code)


class TorHandler(RestHandler):
    """
    Return informations about the current tor status.
    """
    allowed = (
            'version', 'ns/all', 'status/bootstrap-phase',

    )

    @web.asynchronous
    @web.authenticated
    def get(self, sp_keyword='status/bootstrap-phase'):
        """
        Processes GET requests:
            * /tor/<sp_keyword>

        In case the GETINFO command returns a 552 error code, raise a 404.
        (controlspec.txt) «If some of the listed keywords can't be found,
        Tor replies with a "552 Unrecognized option" message.»

        In case tor is not yet started, return a error message in JSON format.
        """
        try:
            self.controller.get(sp_keyword).addCallback(
                    lambda infos: self.finish(json_encode(infos)))
        except ValueError:
            raise web.HTTPError(404)
        except KeyError as exc:
            self.finish(self.error(exc))
        except RuntimeError as exc:
            return self.finish(self.error(exc))


