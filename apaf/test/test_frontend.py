import sys

from twisted.trial import unittest
from twisted.python import log
from twisted.internet import reactor
from cyclone import web

from apaf import config

class MockApplication(web.Application):
    def __init__(self):
        handlers = [
                (r'/', IndexHandler),
        ]
        settings = dict(
                debug=True,
                template_path=config.static_dir,
        )
        web.Application.__init__(self, handlers, **settings)


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    reactor.listenTCP(8888, MockApplication(), interface='127.0.0.1')
    reactor.run()
