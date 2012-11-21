from hashlib import sha256

from cyclone import web

from apaf import config
from apaf.utils import hashing


class PanelHandler(web.RequestHandler):
    """
    The most basic handler, for all handlers.
    """

    _session_cookies = []

    def get_current_user(self):
        """
        Return the current user authenticated.
        """
        return any((
            self._check_session(self.get_secure_cookie('auth')),
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

    def _check_session(self, session_cookie):
        return session_cookie in self._session_cookies

    def _new_session(self):
        session = hashing.random_bytes(32)
        self._session_cookies.append(session)
        return session

    def auth_login(self, passwd):
        if not self._check_pass(passwd):
            return False
        else:
            self.set_secure_cookie('auth', self._new_session())
            return True

    def auth_logout(self):
        session = self.get_secure_cookie('auth')
        try:
            self._session_cookies.remove(session)
        except ValueError:
            return False
        else:
            return True



class IndexHandler(PanelHandler):
    def get(self):
        """
        Process GET request:
            * /
        Should redirect to the js application or the legacy html application
        depending on the browser type
        """
        self.set_header('Content-Type', 'text/plain')
        self.redirect('/index.html')
