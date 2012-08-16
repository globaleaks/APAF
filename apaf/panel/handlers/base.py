from hashlib import sha256

from cyclone import web

from apaf import config
from apaf.utils import hashing


class PanelHandler(web.RequestHandler):
    """
    The most basic handler, for all handlers.
    """
    def get_current_user(self):
        """
        Return the current user authenticated.
        """
        return any((
            self._check_pass(self.get_secure_cookie('auth') or ''),
            #self.request.host == '127.0.0.1',
        ))

    def _check_pass(self, passwd):
        """
        Return true if passwd is valid, false otherwise.
        """
        assert isinstance(passwd, str)
        _passwd = self.application.conf['passwd']
        assert len(_passwd) >= 32

        return hashing.hash(passwd) == _passwd

    def auth_login(self, passwd):
        if not self._check_pass(passwd):
            return False
        else:
            self.set_secure_cookie('auth', passwd)
            return True



class IndexHandler(PanelHandler):
    def get(self):
        """
        Process GET request:
            * /
        """
        print self.request
        self.set_header('Content-Type', 'text/plain')
        self.finish('Hello world')
