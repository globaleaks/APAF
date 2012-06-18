import json

from cyclone import web, escape, auth
import apaf

class PanelHandler(web.RequestHandler):
    """
    A simple RequestHandler with utils for the panel
    """
    def get_logged_user(self):
        pass

    def initialize(self, action):
        self.action = action

    def set_default_headers(self):
        """
        Panel API is performed entirely via json calls.
        """
        #self.set_header("Content-Type", "application/json")

class AuthHandler(PanelHandler, auth.OAuthMixin):
    pass

class ServiceHandler(PanelHandler):
    _actions = ['state', 'start', 'stop']

    @property
    def services(self):
        """
        Return a dictionary service-name:service-class of all instantiated
        services.
        """
        return {service.name:service for service in apaf.hiddenservices}

   # cache decorator here.
    def _get_service(self, name=None):
        if not name in self.services:
            raise web.HTTPError(404)
        else:
            return self.services[name]

    def state(self, service):
        """
        Process GET request:
            * /services/<service>/
        Return a dictionary containig a summary of what the service is and on
        which url is running on.
        """
        keys = ['name', 'desc', 'url']
        return {name:getattr(service, name, None) for name in keys}

    def start(self, service):
        """
        Process GET request:
            * /services/<service>/start
        """

    def stop(self, service):
        """
        Process GET request:
            * /services/<service>/stop
        """

    # @web.authenticated
    def get(self, service=None):
        """
        Processes GET requests:
          * /services/
          * /services/<service>/
          * /services/<service>/start
          * /services/<service>/stop
        """
        if not service:
            resp = self.services.keys()
        elif self.action in self._actions:
            service = self._get_service(service)
            resp = getattr(self, self.action)(service)

        self.finish(escape.json_encode(resp))
