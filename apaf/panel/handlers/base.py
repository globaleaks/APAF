from cyclone import web

from apaf import config

class PanelHandler(web.RequestHandler):
    """
    The most basic handler, for all handlers.
    """
    def get_current_user(self, passwd=None):
        """
        Return the current user authenticated.
        """
        if passwd: return passwd == config.custom['passwd']
        else: return any((
            self.get_secure_cookie('auth') == config.custom['passwd'],
            self.request.remote_ip == '127.0.0.1',
        ))


class IndexHandler(PanelHandler):
    def get(self):
        """
        Process GET request:
            * /
        """
        print self.request
        self.set_header('Content-Type', 'text/plain')
        self.finish('Hello world')
