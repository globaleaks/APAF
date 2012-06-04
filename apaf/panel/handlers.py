import json
from twisted.web.resource import Resource

import apaf

class MenuHandler(Resource):
    def getChild(self, path, request):
        pass

class TorHandler(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.putChild('start', app_start_handler())
        self.putChild('stop', app_stop_handler())
        self.putChild('status', app_status_handler())

    def render_GET(self, request):
        ret = {'options': ['start', 'stop', 'status', 'restart']}
        return json.dumps(ret)

class app_start_handler(Resource):
    def render_GET(self, request):
        ret = {'Result': True}
        return json.dumps(ret)

class app_stop_handler(Resource):
    def render_GET(self, request):
        ret = {'Result': True}
        return json.dumps(ret)

class app_status_handler(Resource):
    def render_GET(self, request):
        ret = {'Result': True}
        return json.dumps(ret)

class AppHandler(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.putChild('start', app_start_handler())
        self.putChild('stop', app_stop_handler())
        self.putChild('status', app_status_handler())
    def render_GET(self, request):
        ret = {'options': ['start', 'stop', 'status', 'restart', 'address']}
        return json.dumps(ret)

class StatusHandler(Resource):
    def render_GET(self, request):
        ret = {'options': ['show', 'update', 'other']}
        return json.dumps(ret)

class ServiceHandler(Resource):
    def _base_attrs(self, service):
        """
        Returns a dictionary containig a summary of what the service is and on
        which url is running on.
        """
        keys = ['name', 'desc', 'url']
        return {name:getattr(service, name, None) for name in keys}

    def render_GET(self, request):
        return json.dumps([self._base_attrs(service)
            for service in apaf.hiddenservices])
